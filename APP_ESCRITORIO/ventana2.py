from tkinter import *
import tkinter as tk
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
import requests
from nidaqmx.errors import DaqError


class Ventana2:
    def __init__(self, menu, ventana_principal):
        super().__init__()
        labelFont = ("Bold Italic", 20, 'bold')

        #Variables
        self._nombre_v2 = tk.StringVar()
        self._corriente_fija = tk.StringVar()
        self._saturacion_campo = tk.StringVar()
        self._tiempo_entre_mediciones_v2 = tk.StringVar()
        self._pasos = tk.StringVar()
        self.LineaTendencia = tk.BooleanVar()

        # Lista para perfiles de parámetros
        self.perfiles_parametros2 = self.cargar_perfiles_desde_archivo()
        self. detener_medicion = False


        #Diseño ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title("Caracterización Magnetoeléctrica")
        widht_menu =1000
        height_menu = 600
        centrar_ventana(self.menu,widht_menu,height_menu )

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Magnetoeléctrica', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.menu, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Entradas
        tk.Label(self.menu, text="Nombre", bg="#A6C3FF").place(x=25, y=60)
        tk.Entry(self.menu, textvariable=self._nombre_v2).place(x=25, y=80, width=210)
        tk.Label(self.menu, text="Corriente Fija(A)", bg="#A6C3FF").place(x=25, y=110)
        tk.Entry(self.menu, textvariable=self._corriente_fija).place(x=25, y=130, width=210)
        tk.Label(self.menu, text="Saturacion de Campo(G)", bg="#A6C3FF").place(x=25, y=160)
        tk.Entry(self.menu, textvariable=self._saturacion_campo).place(x=25, y=180, width=210)
        tk.Label(self.menu, text="Tiempo entre Mediciones(s)", bg="#A6C3FF").place(x=25, y=210)
        tk.Entry(self.menu, textvariable=self._tiempo_entre_mediciones_v2).place(x=25, y=230, width=210)
        tk.Label(self.menu, text="Intervalos de Campos", bg="#A6C3FF").place(x=25, y=260)
        tk.Entry(self.menu, textvariable=self._pasos).place(x=25, y=280, width=210)
        checkbutton = tk.Checkbutton(
            self.menu, 
            text="Línea de Tendencia", 
            variable=self.LineaTendencia, 
            font=("Arial", 7),        # Fuente más pequeña
            padx=2, pady=2,           # Reducir padding
            highlightthickness=0      # Borde de enfoque más pequeño
        )
        checkbutton.place(x=25, y=350)


        #Botones
        btn_volver = tk.Button(self.menu, text='Volver', bg="#99A8EF", command=self.volver)
        btn_volver.place(x=50, y=1.5)
        btn_guardar_perfil = tk.Button(self.menu, text="Guardar Perfil", command=self.guardar_perfil)
        btn_guardar_perfil.place(x=35, y=375)
        btn_cargar_perfil = tk.Button(self.menu, text="Cargar Perfil", command=self.cargar_perfil)
        btn_cargar_perfil.place(x=135, y=375)
        btn_iniciar = tk.Button(self.menu, text="Iniciar", command=self.medir_GV_curve)
        btn_iniciar.place(x=50, y=420)

        btn_obtener_ecuacion = tk.Button(self.menu, text="Obtener ecuacion", command=self.abrir_datosecu)
        btn_obtener_ecuacion.place(x=100, y=420)
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
        self.ax.set_xlabel('G')
        self.ax.set_ylabel('R')
        plt.xlim(-20, 20)
        plt.ylim(-6000, 6000)
        self.ax.grid(True)

        # Crear un lienzo de Tkinter para la figura
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Agregar la barra de herramientas de navegación en la parte inferior
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Mostrar la leyenda solo si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:
            self.ax.legend()

        # Mantener el gráfico arriba
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.rm = None
        self.voltajes = None
        self.array_prom_gauss_volts = []

        #Actualizar Perfiles
        self.cargar_perfiles_desde_archivo()
        self.actualizar_combo_perfiles()

            
    def abrir_datosecu(self):
        self.menuecu = Toplevel()
        self.menuecu.title("Datos Ecuacion")
        widht_menuecu =300
        height_menuecu = 300
        centrar_ventana(self.menuecu,widht_menuecu,height_menuecu )
        self.menuecu.configure(bg="#A6C3FF")
        self.menuecu.grab_set()
        #Variables
        self._start_voltaje = tk.StringVar()
        self._step_size = tk.StringVar()
        self._delay = tk.StringVar()
        
        #Entradas
        tk.Label(self.menuecu, text="Intervalo Simétrico(V)", bg="#A6C3FF").place(x=30, y=20)
        tk.Entry(self.menuecu, textvariable=self._start_voltaje).place(x=30, y=40, width=220)
        tk.Label(self.menuecu, text="Intervalos de Voltajes", bg="#A6C3FF").place(x=30, y=80)
        tk.Entry(self.menuecu, textvariable=self._step_size).place(x=30, y=100, width=220)
        tk.Label(self.menuecu, text="Tiempo entre Mediciones(s)", bg="#A6C3FF").place(x=30, y=140)
        tk.Entry(self.menuecu, textvariable=self._delay).place(x=30, y=160, width=220)

        self.menuecu.transient(self.menu)
        self.menuecu.grab_set()
        
        
        #Botones
        self.boton_cerrar = tk.Button(self.menuecu, text="Cancelar", command=self.destroy)
        self.boton_cerrar.place(x=50, y=220)
        self.boton_calcular = tk.Button(self.menuecu, text="Calcular", command=self.obtener_ecuacion)
        self.boton_calcular.place(x=150, y=220)
    
    def obtener_ecuacion(self):
            array_prom_gauss_volts = []
            def obtener_ecuacion():
                    # Configuración inicial de la fuente     
                    start_voltaje_str = self._start_voltaje.get()
                    step_size_str = self._step_size.get() # Número de pasos
                    delay_str = self._delay.get()
                    if verificar_inputs_ecuacion(start_voltaje_str, step_size_str, delay_str, self.menu):
                        start_voltaje = int(self._start_voltaje.get())
                        step_size = int(self._step_size.get()) # Número de pasos
                        delay = float(self._delay.get())
                        voltajes = np.linspace(start_voltaje, -start_voltaje, num=step_size)  # Genera voltajes 
                        addresses= ["6"]
                        if verificar_dispositivo(addresses, self.menu, False):
                            self.rm = pyvisa.ResourceManager()
                            fuente = self.rm.open_resource('GPIB::6::INSTR')  
                            self.configurar_fuente(fuente) 
                            # Bucle para establecer voltajes
                            try:
                                self.mostrar_mensaje_inicio("Proceso en Curso", "El proceso está en curso. Espere a que termine.")
                                for voltaje in voltajes:
                                    voltaje = round(voltaje, 1)  # Redondear el voltaje
                                    self.detener_medicion = False  # Reiniciar la variable de control
                                    if self.detener_medicion:
                                        break
                                    fuente.write(f'SOUR:VOLT {voltaje}')  # Establecer el voltaje
                                    # Esperar a que se procesen los comandos
                                    time.sleep(delay)  # Espera para permitir la estabilización Min 0.04 para permitir una estabilización pp estuvo aca
                                    array_prom_gauss_volts.append((voltaje,self.obtener_gauss()))#se agrega  promedio de gauss y voltaje a array


                            except pyvisa.errors.VisaIOError as e:
                                messagebox.showerror("Error de VISA:", f"{e}", parent = self.menu)

                            finally:
                                fuente.write("OUTP OFF")  # Apagar después del bucle
                                fuente.write('*CLS')  # Limpiar el estado
                                fuente.write('*RST')  # Reiniciar el sistema
                                fuente.close()  # Cerrar la conexión
                                voltaje, senal_ni = zip(*array_prom_gauss_volts)#Guarda voltaje y señal de gauss respectivamente
                                # Calcular pendiente e intercepto
                                m, b = np.polyfit(voltaje, senal_ni, 1)
                                ecuacion_dia = {
                                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                                    "pendiente": m,
                                    "intercepto": b
                                }
                                
                                # Guardar ecuación del día
                                ruta_archivo = 'utils/ecuaciones/ecuacion.json'
                                os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)  # Crear carpeta si no existe
                                with open(ruta_archivo, 'w') as archivo:
                                    json.dump(ecuacion_dia, archivo, indent=4)
                                    messagebox.showinfo("'Información","Ecuación generada correctamente" , parent=self.menu)

                    # Ejecutar la medición en un hilo separado
            self.hilo_medicion = threading.Thread(target=obtener_ecuacion)
            self.hilo_medicion.start()
    
    def obtener_gauss(self):
            num_samples = 10
            sample_rate = 1000  # en Hz 
            try:
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
                    promedio_data_0 = self.volts_a_gauss(promedio_data_0, probe_type)
                    # Mostrar los resultados
                    return promedio_data_0
            except nidaqmx.DaqError as e:
                messagebox.showwarning("Advertencia",f"Ha ocurrido un error con el GaussMeter,{e}")

    def volts_a_gauss(self, volts, probe_type):
            voltajes_mV = volts * 1000  # Convertir a milivoltios
            if probe_type == 'ST':
                gauss = voltajes_mV / 0.1  # Para HS Probe
            else:
                raise ValueError("Tipo de sonda no reconocido")
            return gauss

    def destroy(self):
            self.__class__.en_uso = False
            return self.menuecu.destroy()
        


    #Guardar perfil de parámetros
    def guardar_perfil(self):
        nombre_v2 = self._nombre_v2.get().strip()
        if not nombre_v2:
            messagebox.showerror("Error", "El nombre del perfil no puede estar vacío.")
            return

        #Validar que los valores sean correctos
        corriente_fija = self._corriente_fija.get().strip()
        saturacion_campo = self._saturacion_campo.get().strip()
        tiempo_entre_mediciones_v2 = self._tiempo_entre_mediciones_v2.get().strip()
        pasos = self._pasos.get().strip()

        if not corriente_fija or not saturacion_campo or not tiempo_entre_mediciones_v2 or not pasos:
            messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return
        
        #Guardar parámetros en el diccionario
        self.perfiles_parametros2[nombre_v2] = {
            "Corriente_fija": corriente_fija,
            "Saturacion_de_campo": saturacion_campo,
            "tiempo_entre_mediciones_v2": tiempo_entre_mediciones_v2,
            "Pasos": pasos
        }

        guardar = validar_perfil_v2(nombre_v2, corriente_fija, saturacion_campo, tiempo_entre_mediciones_v2, pasos)
        if guardar == True:
            self.guardar_perfiles_a_archivo()
            self.actualizar_combo_perfiles()
            messagebox.showinfo("Información", f"Perfil '{nombre_v2}' guardado exitosamente.")
        
    #Cargar perfil de parámetros
    def cargar_perfil(self):
        nombre_v2 = self.combo_perfiles.get()
        if nombre_v2 in self.perfiles_parametros2:
            perfil = self.perfiles_parametros2[nombre_v2]
            self._nombre_v2.set(nombre_v2)
            self._corriente_fija.set(perfil["Corriente_fija"])
            self._saturacion_campo.set(perfil["Saturacion_de_campo"])
            self._tiempo_entre_mediciones_v2.set(perfil["tiempo_entre_mediciones_v2"])
            self._pasos.set(perfil["Pasos"])
            messagebox.showinfo("Información", f"Perfil '{nombre_v2}' cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfil válido para cargar.")

    #Actualizar los parámetros en el ComboBox
    def actualizar_parametros(self, event):
        self.cargar_perfil()

    #Actualizar Combobox
    def actualizar_combo_perfiles(self):
        self.combo_perfiles['values'] = list(self.perfiles_parametros2.keys())
    
    #Cargar Perfil en archivo
    def cargar_perfiles_desde_archivo(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'APP_ESCRITORIO', 'perfiles_parametros2.json')
        
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        try:
            # Intentar abrir el archivo si existe
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    return json.load(file)
            else:
                # Si no existe, crearlo y devolver un diccionario vacío
                with open(json_path, 'w') as file:
                    json.dump({}, file, indent=4)
                return {}
        except json.JSONDecodeError:
            # Manejar archivo corrupto
            messagebox.showerror("Error", "El archivo de perfiles está corrupto. Se creará uno nuevo.")
            with open(json_path, 'w') as file:
                json.dump({}, file, indent=4)
            return {}
        except Exception as e:
            # Manejo de cualquier otro error
            messagebox.showerror("Error", f"Error inesperado al cargar el archivo: {str(e)}")
            return {}

        # Verificar si el archivo existe
        if not os.path.exists(json_path):
            # Si el archivo no existe, crearlo vacío
            with open(json_path, 'w') as file:
                json.dump({}, file, indent=4)
            return {}
        
        try:
            with open(json_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo de perfiles está corrupto. Se creará uno nuevo.")
            with open(json_path, 'w') as file:
                json.dump({}, file, indent=4)
            return {}

    #Guardar Perfil en archivo    
    def guardar_perfiles_a_archivo(self):
        ruta_archivo = os.path.join(os.getcwd(), "perfiles_parametros2.json")
        with open(ruta_archivo, "w") as archivo:
            json.dump(self.perfiles_parametros2, archivo, indent=4)

    # Obtención de entradas
    @property
    def nombre_v2(self):
        return self._nombre_v2.get()

    @property
    def corriente_fija(self):
        return self._corriente_fija.get()

    @property
    def saturacion_campo(self):
        return self._saturacion_campo.get()

    @property
    def tiempo_entre_mediciones_v2(self):
        return self._tiempo_entre_mediciones_v2.get()

    def mostrar_mensaje_inicio(self):
        # Crear una nueva ventana de diálogo personalizada
        self.popup = tk.Toplevel(self.menu)
        self.popup.title("Confirmar Detención")

        # Calcular las dimensiones de la ventana principal
        ventana_principal_width = self.menu.winfo_width()
        ventana_principal_height = self.menu.winfo_height()
        ventana_principal_x = self.menu.winfo_rootx()
        ventana_principal_y = self.menu.winfo_rooty()

        # Definir el tamaño de la ventana emergente
        popup_width = 300
        popup_height = 100

        # Calcular la posición centrada
        x = ventana_principal_x + (ventana_principal_width - popup_width) // 2
        y = ventana_principal_y + (ventana_principal_height - popup_height) // 2

        # Establecer la geometría de la ventana emergente
        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        # Deshabilitar la interacción con la ventana principal
        self.popup.transient(self.menu)
        self.popup.grab_set()

        # Etiqueta con el mensaje
        mensaje_label = tk.Label(self.popup, text="¿Deseas detener la medición?", padx=10, pady=10)
        mensaje_label.pack()

        # Botón para cerrar la ventana y confirmar la detención
        self.boton_cerrar = tk.Button(self.popup, text="Cancelar", command=self.confirmar_detener_medicion)
        self.boton_cerrar.pack(pady=10)

        # Manejar el evento de cierre de la ventana emergente
        self.popup.protocol("WM_DELETE_WINDOW", self.confirmar_detener_medicion)

        # Ejecutar la medición en un hilo separado     
    def cerrar_popup(self):
        self.popup.grab_release()
        self.popup.destroy()
        
    def configurar_fuente(self, fuente):
        fuente.timeout = 1000
        fuente.read_termination = '\n'
        fuente.write_termination = '\n'
        fuente.baud_rate = 57600
        fuente.write('*CLS')
        fuente.write('*RST')
        fuente.write('SOUR:FUNC:MODE VOLT')
        fuente.write('SOUR:CURR 20')
        fuente.write("OUTP ON")

    def configurar_multimetro(self, multimetro, corriente):
        multimetro.write("*RST")
        multimetro.write(":SOUR:FUNC CURR")
        multimetro.write(f":SOUR:CURR {corriente}")
        multimetro.write("CONF:VOLT:DC")
        multimetro.write("OUTPUT ON")

    def medir_voltaje(self, multimetro):
        medida_voltaje = multimetro.query(":MEAS:VOLT:DC?")
        valores = medida_voltaje.strip().split(',')
        return float(valores[0])
        
    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()

    def volts_a_gauss(self, volts, probe_type):
        voltajes_mV = volts * 1000  # Convertir a milivoltios

        if probe_type == 'ST':
            gauss = voltajes_mV / 0.1  # Para HS Probe
        else:
            raise ValueError("Tipo de sonda no reconocido")
        return gauss

    def obtener_gauss(self):
        num_samples = 10
        sample_rate = 1000  # en Hz 
        try:
        
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
                promedio_data_0 = self.volts_a_gauss(promedio_data_0, probe_type)
                # Mostrar los resultados
                return promedio_data_0
        except DaqError as e:
            messagebox.showwarning("Advertencia",f"Ha ocurrido un error con el GaussMeter,{e}")
            

    def cargar_ecuacion_del_dia(self):
        ruta_archivo = 'utils/ecuaciones/ecuacion.json'

        try:
            # Abrir y cargar el archivo JSON
            with open(ruta_archivo, 'r') as archivo:
                ecuacion = json.load(archivo)

            # Obtener la fecha actual
            dia_actual = datetime.now().strftime("%Y-%m-%d")

            # Comparar la fecha de la ecuación con la fecha actual
            if ecuacion['fecha'] == dia_actual:
                m = ecuacion['pendiente']  # Pendiente
                b = ecuacion['intercepto']  # Intercepto
                return m, b
            else:
                messagebox.showerror("Advertencia", f"No hay ecuación disponible para la fecha actual: {dia_actual}. Por favor, genera una nueva",parent=self.menu)
                return False
            

        except FileNotFoundError:
            # Manejar el caso donde el archivo no exista
            messagebox.showwarning("Advertencia", "El archivo de la ecuación no se encontró. Por favor, genera una ecuación nueva.",parent=self.menu)
            return False

    def confirmar_detener_medicion(self):
        # Cambiar la variable de control para detener el hilo
        self.detener_medicion = True
        self.popup.destroy()  # Cerrar la ventana emergente

    def medir_GV_curve(self):
        def ejecutar_medicion():

            constant_current_str =self._corriente_fija.get()
            step_size_str = self._pasos.get()
            delay_str =  self._tiempo_entre_mediciones_v2.get()
            start_saturation_str =  self._saturacion_campo.get() 
            # Validar que todos los valores sean válidos
            if verificar_inputs_gauss(start_saturation_str, constant_current_str, step_size_str, delay_str, self.menu):
                # Continúa con el proceso si no hay errores
                start_current = float(constant_current_str)
                start_saturation = int(start_saturation_str)
                step_size = int(step_size_str)
                delay = float(delay_str)
                self.fields = np.linspace(start_saturation, -start_saturation, num=step_size)
                self.array_prom_gauss_volts = []
                # Inicializar el gestor de recursos VISA
                self.rm = pyvisa.ResourceManager()

                # Abrir la conexión con el multímetro, fuente de poder y realizar la medición
                addresses= ["9","6"]
                if verificar_dispositivo(addresses, self.menu, True):
                    
                    try:

                        self.mostrar_mensaje_inicio()
                        multimetro = self.rm.open_resource('GPIB0::9::INSTR')
                        fuente = self.rm.open_resource('GPIB0::6::INSTR')# Conectar a la fuente de alimentación
                        # Configurar el multímetro para ser una fuente de corriente y medir voltaje
                        self.configurar_multimetro(multimetro, start_current)
                        self.configurar_fuente(fuente)
                        
                        if self.cargar_ecuacion_del_dia() is  not False:  
                            a, b = self.cargar_ecuacion_del_dia()
                            for field in self.fields:
                                
                                self.detener_medicion = False  # Reiniciar la variable de control 
                                if self.detener_medicion:
                                    break
                                deltaV = (field-b)/a
                                deltaV = round(deltaV, 1)  # Redondear el voltaje
                                fuente.write(f'SOUR:VOLT {deltaV}')  # Establecer el voltaje
                                time.sleep(delay)
                                # Medir el voltaje mientras se aplica la corriente
                                V = self.medir_voltaje(multimetro)
                                self.array_prom_gauss_volts.append((start_current, V, deltaV, self.obtener_gauss(),field))#se agrega  promedio de gauss y voltaje a array                            
                            self.menu.after(0, self.boton_cerrar.config, {'state': tk.NORMAL})
                            self.actualizar_interfaz_despues_de_medir()
                            # Apagar la salida después de las mediciones
                            multimetro.write("OUTPUT OFF")
                            fuente.write("OUTP OFF")  # Apagar después del bucle
                            fuente.write('*CLS')  # Limpiar el estado
                            fuente.write('*RST')  # Reiniciar el sistema
                            fuente.close()  # Cerrar la conexión
                            multimetro.write("OUTPUT OFF")
                            multimetro.close()

                        

                    except pyvisa.errors.VisaIOError as e:
                        if 'VI_ERROR_LIBRARY_NFOUND' in str(e):
                            messagebox.showerror("'VI_ERROR_LIBRARY_NFOUND","Error: No se pudo localizar o cargar la biblioteca requerida por VISA. Verifique que los controladores VISA estén instalados correctamente y el software NI-VISA esté instalado." , parent=self.menu)
                        else:
                            messagebox.showerror("'Error inesperado de VISA",f"{e}" , parent=self.menu)

        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar_medicion)
        self.hilo_medicion.start()




    def guardar_prueba(self,event=None):  # Accept the event argument from Tkinter
            nombre_v2=self.nombre_v2
            tiempo_entre_mediciones_v2=self.tiempo_entre_mediciones_v2
            corriente_fija=self.corriente_fija
            if not (isinstance(self.array_prom_gauss_volts, np.ndarray) and self.array_prom_gauss_volts.size > 0 and not np.all(self.array_prom_gauss_volts == 0)) and self.array_prom_gauss_volts:
            
                # Obtener el título actual de la ventana como sugerencia de nombre_v2
                proyecto_titulo = "test_gauss_"
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], initialfile=proyecto_titulo)
                
                m, b = self.cargar_ecuacion_del_dia()
                
                if file_path:  # Si el usuario no cancela la selección del archivo
                    with open(file_path, 'w') as file:
                        file.write(f"Ecuación:{m:.6f}x {b:.6f}, Saturación de campo:{self._saturacion_campo.get()}, tiempo entre mediciones:{self._tiempo_entre_mediciones_v2.get()}, Pasos:{self._pasos.get()}\n\n")
                        file.write("\tCorriente Fija\t\tMedida Voltaje\t\tR\t\tDelta V\t\tGauss Teórico\t\tGauss Real\n\n")

                        for start_current, V, deltaV, saturacion, field in self.array_prom_gauss_volts:
                            file.write(f"{start_current}\t\t{V:.6f}\t\t{(V/start_current):.6f}\t\t{deltaV:.6f}\t\t{saturacion:.6f}\t\t{field}\n")
                    messagebox.showinfo("\tInformación", f"Datos guardados en: {file_path}")
                
                # Verificar si el servidor API está activo antes de ejecutar `enviar_datos_completos`
                url_ping = "http://127.0.0.1:8000"  # Dirección base de tu servidor API (puedes cambiarla si es diferente)
                try:
                    response = requests.get(url_ping)
                    if response.status_code == 200:
                        print("Servidor API activo. Ejecutando `enviar_datos_completos`...")
                        self.enviar_datos_completos(nombre_v2, tiempo_entre_mediciones_v2,corriente_fija)
                    else:
                        messagebox.showwarning("Advertencia", "El servidor API no está activo. Los datos no se enviarán.")
                except requests.exceptions.RequestException as e:
                    # Si el servidor no responde o hay problemas de conexión
                    print(f"Error al intentar conectar con el servidor API: {e}")
                    messagebox.showwarning("Advertencia", "No se puede conectar al servidor API. Los datos no se enviarán.")
            else:
                messagebox.showwarning("Advertencia", "No hay datos para guardar. Realiza la medición primero.")



    def actualizar_interfaz_despues_de_medir(self):
        self.confirmar_detener_medicion()
        self.menu.after(0, self.mostrar_grafico(), "Información", "Medición completada")
    
    def mostrar_mensaje(self, titulo, mensaje):
        # Muestra un mensaje en el hilo principal
        messagebox.showinfo(titulo, mensaje)
        # Muestra el gráfico en el hilo principal
        self.mostrar_grafico()


    def calcular_resistencia(self):
                # Escribir los datos en filas
        resistencia_promedio_array =[]
        saturacion_array = []
        for i in range(0, len(self.array_prom_gauss_volts)):  # Avanzar de dos en dos (pares: desactivado, activado)   
            desactivado = self.array_prom_gauss_volts[i]
            current1 = desactivado[0]
            voltaje1 = desactivado[1]

            r1 = voltaje1/current1
           
            resistencia_promedio_array.append(r1)
            saturacion_array.append( desactivado[3])
        return resistencia_promedio_array, saturacion_array

    def mostrar_grafico(self):
        try:
            start_current,V, deltaV, saturacion,field = zip(*self.array_prom_gauss_volts)

        except ValueError:
            messagebox.showerror("Error:", "self.resultados no tiene el formato esperado", parent = self.menu)
            return

        #G vs V
        resistencia_calculada, saturacion = self.calcular_resistencia()
        # Graficar los datos experimentales con una etiqueta
        self.ax.plot(saturacion, resistencia_calculada, marker='o', linestyle='-', label='Datos Experimentales')
        # Ajustar una línea de tendencia
        grado = 1
        coeficientes = np.polyfit(saturacion, resistencia_calculada, grado)
        resistencia = 1 / coeficientes[0]
        self._R=resistencia
        if self.LineaTendencia.get():
            # Calcular la línea de tendencia usando corrientes para el eje x
            tendencia = np.polyval(coeficientes, resistencia_calculada)
            self.ax.plot(saturacion, tendencia, '--', label=f'Tendencia Lineal (R = {resistencia:.4f} ohms)')
        # Mostrar la leyenda solo si hay etiquetas definidas
        handles = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()
        self.ax.set_xlim(min(saturacion) - 20, max(saturacion) + 20)
        plt.ylim(resistencia_calculada[-1] - 100, resistencia_calculada[0]+100)
        self.ax.grid(True)
        self.canvas.draw()

    def borrar_grafico(self):
                # Agregar un marco para contener el gráfico y la barra de herramientas
        self.ax.grid(True)

        self.ax.clear()  # Limpiar el eje actual
        self.ax.set_title('Gráfico')
        self.ax.set_ylabel('R')
        self.ax.set_xlabel('G')
        plt.xlim(-20,20)
        plt.ylim(-6000,6000)
                # Mostrar la leyenda solo si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:  # Solo mostrar la leyenda si hay etiquetas
            self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()

    def enviar_datos_completos(self, nombre_v2, tiempo_entre_mediciones_v2,corriente_fija):
        
        url = "http://127.0.0.1:8000/caracterizacion/api_parametro/"

        try:
            # Convertir valores a flotantes
            tiempo_entre_mediciones_v2 = float(tiempo_entre_mediciones_v2)
        except ValueError:
            print("Error: Asegúrese de ingresar valores numéricos válidos para los intervalos y el tiempo entre mediciones.")
            return None
        # Obtener pendiente e intercepto
        m, b = self.cargar_ecuacion_del_dia()

        pendiente, intercepto = m,b

        # Construcción del JSON con los datos básicos
        data = {
            "perfil_parametro_name": nombre_v2,
            "intervalo_simetrico": 0,
            "intervalo_corriente": 0,
            "delay": tiempo_entre_mediciones_v2,
            "bloqueado": False,
            "fija_corriente": corriente_fija,
            "pruebas": []
        }

        # Generar las pruebas y mediciones
        prueba = {
            "prueba_name": nombre_v2,
            "tipo": "Caracterización Magnetoeléctrica",
            "pendiente": float(f"{pendiente:.6f}"),
            "intercepto": float(f"{intercepto:.6f}"),
            "mediciones": []
        }

        # Asegúrate de que `self.array_prom_gauss_volts` contiene las mediciones realizadas
        if not getattr(self, "array_prom_gauss_volts", None):
            print("Advertencia: No hay datos de medición disponibles para enviar.")
            return None

        for start_current, V, deltaV, saturacion, field in self.array_prom_gauss_volts:
            resistencia = round(V / start_current, 6) if start_current != 0 else None
            prueba["mediciones"].append({
                "corriente": round(start_current, 6),
                "voltaje": round(V, 6),
                "resistencia": resistencia,
                "delta_v": deltaV,
                "campo": field,
                "saturacion_campo": saturacion,
                "fecha": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            })

        # Agregar la prueba a los datos principales
        data["pruebas"].append(prueba)

        headers = {"Content-Type": "application/json"}

        try:
            # Enviar el POST request con los datos
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                print("Perfil de Parámetro y pruebas creados exitosamente!")
                print(json.dumps(data, indent=4))
                return response.json()
            else:
                print(f"Error al crear el perfil: {response.status_code}")
                print("Detalle:", response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error en la conexión: {e}")
            return None

    