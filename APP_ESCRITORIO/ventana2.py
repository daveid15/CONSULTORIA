from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
import numpy as np
import pyvisa
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading 
from validacion import *
import json
import nidaqmx

class Ventana2:
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')

        #Variables
        self._nombre = tk.StringVar()
        self._corriente_fija = tk.StringVar()
        self._saturacion_campo = tk.StringVar()
        self._tiempo_entre_mediciones = tk.StringVar()
        self._pasos = tk.StringVar()

         # Lista para perfiles de parámetros
        self.perfiles_ventana2 = self.cargar_perfiles_desde_archivo()

        #Diseño ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title("Caracterización Magnetoeléctrica")
        self.menu.geometry("1000x600")

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Magnetoeléctrica', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.menu, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Entradas
        tk.Label(self.menu, text="Nombre", bg="#A6C3FF").place(x=25, y=60)
        tk.Entry(self.menu, textvariable=self._nombre).place(x=25, y=80, width=210)
        tk.Label(self.menu, text="Corriente Fija", bg="#A6C3FF").place(x=25, y=110)
        tk.Entry(self.menu, textvariable=self._corriente_fija).place(x=25, y=130, width=210)
        tk.Label(self.menu, text="Saturacion de Campo", bg="#A6C3FF").place(x=25, y=160)
        tk.Entry(self.menu, textvariable=self._saturacion_campo).place(x=25, y=180, width=210)

        tk.Label(self.menu, text="Tiempo entre Mediciones", bg="#A6C3FF").place(x=25, y=210)
        tk.Entry(self.menu, textvariable=self._tiempo_entre_mediciones).place(x=25, y=230, width=210)
        
        tk.Label(self.menu, text="Pasos", bg="#A6C3FF").place(x=25, y=260)
        tk.Entry(self.menu, textvariable=self._pasos).place(x=25, y=280, width=210)

        #Botones
        btn_volver = tk.Button(self.menu, text="volver", bg="#99A8EF", command=self.volver)
        btn_volver.place(x=50, y=1.5)
        btn_guardar_perfil = tk.Button(self.menu, text="Guardar Perfil", command=self.guardar_perfil)
        btn_guardar_perfil.place(x=35, y=375)
        btn_cargar_perfil = tk.Button(self.menu, text="Cargar Perfil", command=self.cargar_perfil)
        btn_cargar_perfil.place(x=135, y=375)
        btn_iniciar = tk.Button(self.menu, text="Iniciar", command=self.graficar)
        btn_iniciar.place(x=100, y=420)
        btn_guardar_prueba = tk.Button(self.menu, text="Guardar Prueba", command=self.guardar_prueba)
        btn_guardar_prueba.place(x=75, y=465)
        self.btn_clear_plot = tk.Button(self.menu, text="Borrar Gráfico", command=self.borrar_grafico)
        self.btn_clear_plot.place(x=80, y=510)
        #tk.Checkbutton(self.menu, text="Línea de Tendencia", variable=self.LineaTendencia).place(x=50, y=330)

        # ComboBox para seleccionar perfiles de parámetros
        tk.Label(self.menu, text="Perfiles de Parámetros Guardados", bg="#A6C3FF").place(x=25, y=310)
        self.combo_perfiles = tk.ttk.Combobox(self.menu, state="readonly")
        self.combo_perfiles.place(x=25, y=330, width=200)
        self.combo_perfiles.bind("<<ComboboxSelected>>", self.actualizar_parametros)

        # Fecha
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        etiqueta_fecha = tk.Label(self.menu, text=f"Fecha: {fecha_actual}", font=("Arial", 10))
        etiqueta_fecha.place(x=800, y=5)
        
        # Agregar un marco para contener el gráfico y la barra de herramientas
        self.frame_plot = tk.Frame(self.menu)
        self.frame_plot.place(x=300, y=50, width=700, height=500)

        # Configurar la figura de Matplotlib y el eje
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title('Gráfico')
        self.ax.set_xlabel('(H)')
        plt.xlim(-5,5)
        self.ax.set_ylabel('Resistencia (R)')
        plt.ylim(-8,8)
        self.ax.legend()
        self.ax.grid(True)

        # Crear un lienzo de Tkinter para la figura
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Agregar la barra de herramientas de navegación en la parte inferior
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)  # Mover la barra de herramientas abajo

        # Mantener el gráfico arriba
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)        
        self.rm = None
        self.corrientes_fija = None

        #Actualizar Perfiles
        self.cargar_perfiles_desde_archivo()
        self.actualizar_combo_perfiles()

    #Guardar perfil de parámetros
    def guardar_perfil(self):
        nombre = self._nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del perfil no puede estar vacío.")
            return

        #Validar que los valores sean correctos
        corriente_fija = self._corriente_fija.get().strip()
        saturacion_campo = self._saturacion_campo.get().strip()
        tiempo_entre_mediciones = self._tiempo_entre_mediciones.get().strip()

        if not corriente_fija or not saturacion_campo or not tiempo_entre_mediciones:
            messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return
        
        #Guardar parámetros en el diccionario
        self.perfiles_ventana2[nombre] = {
            "Corriente_fija": corriente_fija,
            "Saturacion_de_campo": saturacion_campo,
            "Tiempo_entre_mediciones": tiempo_entre_mediciones
        }
        self.guardar_perfiles_a_archivo()

        #Actualizar el ComboBox con los perfiles guardados
        self.actualizar_combo_perfiles()
        messagebox.showinfo("Información", f"Perfil '{nombre}' guardado exitosamente.")
        
    #Cargar perfil de parámetros
    def cargar_perfil(self):
        nombre = self.combo_perfiles.get()
        if nombre in self.perfiles_ventana2:
            perfil = self.perfiles_parametros_v2[nombre]
            self._nombre.set(nombre)
            self._corriente_fija.set(perfil["corriente_fija"])
            self._saturacion_campo.set(perfil["saturación_campo"])
            self._tiempo_entre_mediciones.set(perfil["tiempo_entre_mediciones"])
            messagebox.showinfo("Información", f"Perfil '{nombre}' cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfil válido para cargar.")

    #Actualizar los parámetros en el ComboBox
    def actualizar_parametros(self, event):
        self.cargar_perfil()

    #Actualizar Combobox
    def actualizar_combo_perfiles(self):
        self.combo_perfiles['values'] = list(self.perfiles_ventana2.keys())
    
    #Cargar Perfil en archivo
    def cargar_perfiles_desde_archivo(self):
        try:
            with open("APP_ESCRITORIO\perfiles_ventana2.json", "r") as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    #Guardar Perfil en archivo    
    def guardar_perfiles_a_archivo(self):
        with open("APP_ESCRITORIO\perfiles_ventana2.json", "w") as archivo:
            json.dump(self.perfiles_ventana2, archivo, indent=4)

    # Obtención de entradas
    @property
    def nombre(self):
        return self._nombre.get()

    @property
    def corriente_fija(self):
        return self._corriente_fija.get()

    @property
    def saturacion_campo(self):
        return self._saturacion_campo.get()

    @property
    def tiempo_entre_mediciones(self):
        return self._tiempo_entre_mediciones.get()


    def iniciar(self):
        print("Iniciado")
        
    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()


    def obtener_gauss(self):
        num_samples = 10
        sample_rate = 1000  # en Hz 
        try:

            def volts_a_gauss(volts, probe_type):
    
                voltajes_mV = volts * 1000  # Convertir a milivoltios

                if probe_type == 'ST':
                    gauss = voltajes_mV / 0.1  # Para HS Probe
                else:
                    raise ValueError("Tipo de sonda no reconocido")
                return gauss
        
            with nidaqmx.Task() as task:

                task.ai_channels.add_ai_voltage_chan("Dev2/ai0")  # Se lee datos de canal 0 de Dev2
                task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)#se configura la obtención de datos de gauss
                # Leer los datos
                data = task.read(num_samples)
                # Convertir los datos a un array de numpy
                data_array_0 = np.array(data[0])  # Datos del canal 0
                promedio_data_0 = np.mean(data_array_0)#Se promedian dato

                # Usar la sonda ST
                probe_type = 'ST'  
                # Convertir a Gauss
                promedio_data_0 = volts_a_gauss(promedio_data_0,probe_type)
                # Mostrar los resultados
                return promedio_data_0
        except nidaqmx.DaqError as e:
            print("Ocurrió un error durante la adquisición de datos:", e)

    def correr_ecuacion(self):
        array_prom_gauss_volts = []
        def obtener_ecuacion():
            try:
                # Configuración inicial de la fuente
                fuente = self.rm.open_resource('GPIB::6::INSTR')  
                fuente.timeout = 1000  #Se establece tiempo de respuesta max
                fuente.read_termination = '\n' #Salto de linea al terminar de leer
                fuente.write_termination = '\n'#Salto de linea al terminar de escribir
                fuente.baud_rate = 57600 #se configura la velocidad de comunicación
                fuente.write('*CLS')  # Limpiar el estado
                fuente.write('*RST')  # Reiniciar la fuente
                fuente.write('SOUR:FUNC:MODE VOLT')  # Establecer en modo voltaje
                fuente.write('SOUR:CURR 20')  # Establecer límite de corriente a 20 A
                fuente.write("OUTP ON")  # Activar la salida       
                start_voltaje = 20
                step_size = 40  # Número de pasos
                delay = 5
                voltajes = np.linspace(start_voltaje, -start_voltaje, num=step_size)  # Genera voltajes 
    # Bucle para establecer voltajes
                for voltaje in voltajes:
                    voltaje = round(voltaje, 1)  # Redondear el voltaje
                    if -20 <= voltaje <= 20:  # Asegurar que el voltaje esté dentro del rango
                        fuente.write(f'SOUR:VOLT {voltaje}')  # Establecer el voltaje
                        print(f"Set voltage to: {voltaje}")  # Imprimir el voltaje establecido
                        # Esperar a que se procesen los comandos
                        time.sleep(delay)  # Espera para permitir la estabilización Min 0.04 para permitir una estabilización pp estuvo aca
                        array_prom_gauss_volts.append((voltaje,self.obtener_gauss()))#se agrega  promedio de gauss y voltaje a array

                    else:
                        print(f"Voltage {voltaje} out of range")

            except pyvisa.errors.VisaIOError as e:
                print("Error de VISA:", e)

            finally:
                fuente.write("OUTP OFF")  # Apagar después del bucle
                fuente.write('*CLS')  # Limpiar el estado
                fuente.write('*RST')  # Reiniciar el sistema
                fuente.close()  # Cerrar la conexión
                voltaje, senal_ni = zip(*array_prom_gauss_volts)#Guarda voltaje y señal de gauss respectivamente
                # Calcular pendiente e intercepto
                m, b = np.polyfit(voltaje, senal_ni, 1)
                return m, b #retorna pendiente e interecepto





    def medir_GV_curve(self):
        def ejecutar_medicion():
            self._corriente_fija = tk.StringVar()
            self._saturacion_campo = tk.StringVar()
            self._tiempo_entre_mediciones = tk.StringVar()
            self._pasos = tk.StringVar()
            constant_current_str =self._corriente_fija.get()
            step_size_str = self._pasos.get()
            delay_str =  self._tiempo_entre_mediciones.get()
            start_saturation_str =  self._saturacion_campo.get() 
            # Validar que todos los valores sean válidos
            if verificar_inputs_gauss(start_saturation_str, constant_current_str, step_size_str, delay_str, self.menu):
                # Continúa con el proceso si no hay errores
                start_current = float(constant_current_str)
                start_saturation = int(start_saturation_str)
                step_size = int(step_size_str)
                delay = float(delay_str)
                self.fields = np.linspace(start_saturation, -start_saturation, num=step_size)
                self.resultados = []
                # Inicializar el gestor de recursos VISA
                self.rm = pyvisa.ResourceManager()
                self.mostrar_mensaje_inicio("Proceso en Curso", "El proceso está en curso. Espere a que termine.")
                # Abrir la conexión con el multímetro y realizar la medición
                if verificar_dispositivo("9", self.menu):
                    try:
                        multimetro = self.rm.open_resource('GPIB0::9::INSTR')
                        fuente = self.rm.open_resource('GPIB0::6::INSTR')# Conectar a la fuente de alimentación
                        # Configurar el multímetro para ser una fuente de corriente y medir voltaje
                        multimetro.write("*RST")  # Resetear el equipo
                        multimetro.write(":SOUR:FUNC CURR")  # Configurar como fuente de corriente
                        multimetro.write(f":SOUR:CURR {start_current}") #se configura corriente fija
                        multimetro.write("CONF:VOLT:DC")  # Configurar para medir voltaje
                        # Encender la salida
                        multimetro.write("OUTPUT ON")
                        
                        
                        # Configuración inicial de la fuente            
                        fuente.timeout = 1000  #Se establece tiempo de respuesta max
                        fuente.read_termination = '\n' #Salto de linea al terminar de leer
                        fuente.write_termination = '\n'#Salto de linea al terminar de escribir
                        fuente.baud_rate = 57600 #se configura la velocidad de comunicación
                        fuente.write('*CLS')  # Limpiar el estado
                        fuente.write('*RST')  # Reiniciar la fuente
                        fuente.write('SOUR:FUNC:MODE VOLT')  # Establecer en modo voltaje
                        fuente.write('SOUR:CURR 20')  # Establecer límite de corriente a 20 A
                        fuente.write("OUTP ON")  # Activar la salida   

                        for field in self.fields:
                            try:
                                # Aplicar la corriente
                                time.sleep(delay)
                                # Medir el voltaje mientras se aplica la corriente
                                medida_voltaje = multimetro.query(":MEAS:VOLT:DC?")
                                valores = medida_voltaje.strip().split(',')
                                
                                V = float(valores[0])
                                self.resultados.append((start_current, V))
                                #print(f"{corriente}, {V}")
                        

                            except pyvisa.errors.VisaIOError as e:
                                print(f"Error de VISA: {e}")
                                self.resultados.append((corriente, None))

                            except ValueError as e:
                                print(f"Error en los valores obtenidos: {e}")
                                self.resultados.append((corriente, None))
                            
                        self.menu.after(0, self.boton_cerrar.config, {'state': tk.NORMAL})
                        self.actualizar_interfaz_despues_de_medir()
                        # Apagar la salida después de las mediciones
                        multimetro.write("OUTPUT OFF")

                    except pyvisa.errors.VisaIOError as e:
                        if 'VI_ERROR_LIBRARY_NFOUND' in str(e):
                            print("Error: No se pudo localizar o cargar la biblioteca requerida por VISA. Verifique que los controladores VISA estén instalados correctamente.")
                            print("Solución recomendada: Asegúrese de que el software NI-VISA (o su equivalente) esté instalado y correctamente configurado.")
                        else:
                            print(f"Error inesperado de VISA: {e}")
            else:
                print("Entradas no válidas, verifique los datos.")

        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar_medicion)
        self.hilo_medicion.start()



    def guardar_prueba(self, event=None):  #Accept the event argument from Tkinter
        if self.resistencia is not None and self.resultados is not None:
            # Obtener el título actual de la ventana como sugerencia de nombre
            proyecto_titulo = "test_"
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")],initialfile=proyecto_titulo)
            if file_path:  # Si el usuario no cancela la selección del archivo
                with open(file_path, 'w') as file:
                    file.write("Resistencia (R)\t(H)\n\n")
                    #
                    for resistencia, voltaje in self.resultados:
                        file.write(f"{resistencia:.3f}\t\t{voltaje}\n")
                messagebox.showinfo("Información", f"Datos guardados en: {file_path}")
            else:
                print("Guardado cancelado.")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para guardar. Realiza la medición primero.")

    def graficar_histeresis(self):
        try:
            corrientes_fija, saturacion = zip(*self.resultados)
        except ValueError:
            print("Error: self.resultados no tiene el formato esperado.")
            return

        # Graficar los datos experimentales con una etiqueta
        self.ax.plot(corrientes_fija, saturacion, marker='o', linestyle='-', label='Curva de Histéresis')

        # Mostrar la leyenda solo si hay etiquetas definidas
        handles = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()
        else:
            print("No se encontraron artistas con etiquetas para la leyenda.")

        self.ax.grid(True)
        self.canvas.draw()

    def graficar(self):
        def ejecutar():
            corriente = self._corriente_fija.get()
            saturacion =self._saturacion_campo.get()
            tiempo = self._tiempo_entre_mediciones.get()
            #Validar que los datos sean correctos
            if verificar_inputs(corriente, saturacion, tiempo):
                corriente=float(corriente)
                saturacion=float(saturacion)
                tiempo=float(tiempo)
                self.corrientes_fija=np.linspace(corriente, -corriente, num=saturacion)
                self.resultados=[]
                self.rm =pyvisa.ResourceManager
                self.mostrar_mensaje_inicio("Proceso en Curso", "El proceso está en curso. Espere a que termine.")
                # Abrir la conexión con el multímetro y realizar la medición
                if verificar_dispositivo("9", self.menu):
                    try:
                        with self.rm.open_resource('GPIB0::9::INSTR') as gaussmeter:
                            # Configurar gaussmeter
                            gaussmeter.write("*RST")  # Resetear el equipo
                            gaussmeter.write(":SOUR:FUNC CURR")  # Configurar como fuente de corriente
                            gaussmeter.write("CONF:VOLT:DC")  # Configurar para medir 
                            # Encender la salida
                            gaussmeter.write("OUTPUT ON")
                            for corriente in self.corrientes_fija:
                                try:
                                    # Aplicar la corriente
                                    gaussmeter.write(f":SOUR:CURR {corriente}")
                                    time.sleep(tiempo)
                                    # Medir 
                                    medida= gaussmeter.query(":MEAS:VOLT:DC?")
                                    valores = medida.strip().split(',')
                                    V = float(valores[0])
                                    self.resultados.append((corriente, V))
                                except pyvisa.errors.VisaIOError as e:
                                    print(f"Error de VISA: {e}")
                                    self.resultados.append((corriente, None))
    
                                except ValueError as e:
                                    print(f"Error en los valores obtenidos: {e}")
                                    self.resultados.append((corriente, None))
    
                            self.menu.after(0, self.boton_cerrar.config, {'state': tk.NORMAL})
                            self.actualizar_interfaz_despues_de_medir()
                            # Apagar la salida después de las mediciones
                            gaussmeter.write("OUTPUT OFF")
                            self.graficar_histeresis()  # Llamar a la función para graficar la curva de histéresis
                    except pyvisa.errors.VisaIOError as e:
                        if 'VI_ERROR_LIBRARY_NFOUND' in str(e):
                            print("Error: No se pudo localizar o cargar la biblioteca requerida por VISA. Verifique que los controladores VISA estén instalados correctamente.")
                            print("Solución recomendada: Asegúrese de que el software NI-VISA (o su equivalente) esté instalado y correctamente configurado.")
                        else:
                            print(f"Error inesperado de VISA: {e}")
                else:
                    print("Entradas no válidas, verifique los datos.")

        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar)
        self.hilo_medicion.start()

    def mostrar_grafico(self):
        try:
            corrientes_fija, saturacion = zip(*self.resultados)
        except ValueError:
            print("Error: self.resultados no tiene el formato esperado.")
            return

        # Graficar los datos experimentales con una etiqueta
        self.ax.plot(corrientes_fija, saturacion, marker='o', linestyle='-', label='Datos Experimentales')

        # Mostrar la leyenda solo si hay etiquetas definidas
        handles = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()
        else:
            print("No se encontraron artistas con etiquetas para la leyenda.")

        self.ax.grid(True)
        self.canvas.draw()

    def borrar_grafico(self):
        self.ax.set_title('Gráfico')
        self.ax.clear()  # Limpiar el eje actual
        self.ax.set_ylabel('Resistencia (R)')
        self.ax.set_xlabel('(H)')
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

