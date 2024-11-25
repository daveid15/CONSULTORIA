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
from nidaqmx.errors import DaqError
from nidaqmx.constants import LineGrouping
relay_pins = ['Dev2/port0/line0', 'Dev2/port0/line1', 'Dev2/port0/line2', 'Dev2/port0/line3']


configuraciones = [
    ((True, False, False, True), "Aplicar Configuración 1", "1 Aplicada"),
    ((True, False, True, False), "Aplicar Configuración 2", "2 Aplicada"),
    ((False, True, False, True), "Aplicar Configuración 3", "3 Aplicada"),
    ((False, True, True, False), "Aplicar Configuración 4", "4 Aplicada")
]

class Ventana3:
    def __init__(self, menu, ventana_principal):
        super().__init__()
        labelFont = ("Bold Italic", 20, 'bold')

        # Variables específicas para Ventana 3
        self._nombre_v3 = tk.StringVar()
        self._corriente_fija_v3 = tk.StringVar()
        self._saturacion_campo_v3 = tk.StringVar()
        self._tiempo_entre_mediciones_v3 = tk.StringVar()
        self._pasos_v3 = tk.StringVar()
        self.LineaTendencia_v3 = tk.BooleanVar()

        # Lista para perfiles de parámetros (Ventana 3)
        self.perfiles_ventana3 = self.cargar_perfiles_desde_archivo()
        self.detener_medicion = False
        self.array_prom_gauss_volts = []

        # Variable para almacenar la instancia de la ventana de relés (Validación)
        self.ventana_reles = None  

        #Descripción configuracion reles
        self.descripcion_configuracion = "Ninguna configuración aplicada"

        #Diseño ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title("Caracterización Magnetoeléctrica Invertida")
        widht_menu =1000
        height_menu = 600
        centrar_ventana(self.menu,widht_menu,height_menu )

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Magnetoeléctrica Invertida', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.menu, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Entradas
        tk.Label(self.menu, text="Nombre", bg="#A6C3FF").place(x=25, y=60)
        tk.Entry(self.menu, textvariable=self._nombre_v3).place(x=25, y=80, width=210)
        tk.Label(self.menu, text="Corriente Fija (A)", bg="#A6C3FF").place(x=25, y=110)
        tk.Entry(self.menu, textvariable=self._corriente_fija_v3).place(x=25, y=130, width=210)
        tk.Label(self.menu, text="Saturación de Campo (G)", bg="#A6C3FF").place(x=25, y=160)
        tk.Entry(self.menu, textvariable=self._saturacion_campo_v3).place(x=25, y=180, width=210)
        tk.Label(self.menu, text="Tiempo entre Mediciones (s)", bg="#A6C3FF").place(x=25, y=210)
        tk.Entry(self.menu, textvariable=self._tiempo_entre_mediciones_v3).place(x=25, y=230, width=210)
        tk.Label(self.menu, text="Intervalos de Campos", bg="#A6C3FF").place(x=25, y=260)
        tk.Entry(self.menu, textvariable=self._pasos_v3).place(x=25, y=280, width=210)

        checkbutton = tk.Checkbutton(
            self.menu, 
            text="Línea de Tendencia", 
            variable=self.LineaTendencia_v3, 
            font=("Arial", 7),        
            padx=2, pady=2,          
            highlightthickness=0
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
        btn_guardar_prueba.place(x=50, y=465)
        btn_reles = tk.Button(self.menu, text="Control de Relés", command=self.abrir_ventana_reles)
        btn_reles.place(x=150, y=465)

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
        plt.xlim(-6000, 6000)
        plt.ylim(-20, 20)
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
        self.array_prom_gauss_volts = None

        #Actualizar Perfiles
        self.cargar_perfiles_desde_archivo()
        self.actualizar_combo_perfiles()

        # Configuración reles en Default al iniciar
        self.relay_states = [tk.BooleanVar(value=False) for _ in relay_pins]
        self.encender_todos_reles()
        

            
    def abrir_datosecu(self):
        self.menuecu = Toplevel()
        self.menuecu.title("Datos Ecuacion")
        widht_menuecu =300
        height_menuecu = 300
        centrar_ventana(self.menuecu,widht_menuecu,height_menuecu )
        self.menuecu.configure(bg="#A6C3FF")
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
                            self.mostrar_mensaje_inicio()
                            # Bucle para establecer voltajes
                            try:
                                self.detener_medicion = False  # Reiniciar la variable de control
                                for voltaje in voltajes:
                                    voltaje = round(voltaje, 1)  # Redondear el voltaje
                                    
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
        

    def abrir_ventana_reles(self):
        if self.ventana_reles is None or not tk.Toplevel.winfo_exists(self.ventana_reles):
            self.ventana_reles = tk.Toplevel(self.menu)
            self.ventana_reles.title("Control de Relés")
            self.ventana_reles.geometry("400x400")
            self.ventana_reles.configure(bg="#A6C3FF")

            self.relay_states = [tk.BooleanVar(value=estado) for estado in self.obtener_estado_actual_reles()]

            # Crear los controles de relés
            for i in range(4):
                tk.Checkbutton(
                    self.ventana_reles,
                    text=f"Relé {i+1}",
                    variable=self.relay_states[i],
                    bg="#A6C3FF",
                    command=lambda i=i: self.actualizar_estado_rele(i)
                ).grid(row=i, column=0, pady=5)

            # Botones para configuraciones
            for i, (estados, label, descripcion) in enumerate(configuraciones, start=0):
                tk.Button(self.ventana_reles, text=label, command=lambda e=estados, d=descripcion: self.aplicar_configuracion(e, d)).grid(row=i, column=1, padx=10)

            # Botones adicionales
            tk.Button(self.ventana_reles, text="Encender Todos", command=self.apagar_todos_reles).grid(row=4, column=0, pady=10)
            tk.Button(self.ventana_reles, text="Apagar Todos", command=self.encender_todos_reles).grid(row=4, column=1, pady=10)

            # Mensaje de estado
            self.texto_estado = tk.Label(self.ventana_reles, text="", bg="#A6C3FF", fg="black")
            self.texto_estado.grid(row=6, columnspan=2, pady=10)

            # Botón para cerrar
            tk.Button(self.ventana_reles, text="Cerrar", command=self.cerrar_ventana_reles).grid(row=7, columnspan=2, pady=10)

            # Control del cierre
            self.ventana_reles.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_reles)

    def obtener_estado_actual_reles(self):
        """
        Obtiene el estado actual de los relés.
        """
        return [var.get() for var in self.relay_states] if hasattr(self, 'relay_states') else [False] * 4
    
    def actualizar_checkboxes(self, estados):
        """
        Sincroniza los checkboxs con el estado actual de los relés.
        """
        for i, estado in enumerate(estados):
            self.relay_states[i].set(estado)


    def cerrar_ventana_reles(self):
        self.ventana_reles.destroy()
        self.ventana_reles = None

    def actualizar_estado_rele(self, index):
        """
        Actualiza el estado de un relé específico.
        """
        estado = self.relay_states[index].get()
        estados = [var.get() for var in self.relay_states]
        self.cambiar_estado_reles(estados)

        # Generar la descripción manual
        self.descripcion_configuracion = ", ".join(["T" if estado else "F" for estado in estados])

        self.mostrar_estado(f"Relé {index+1} {'encendido' if estado else 'apagado'}", "blue" if estado else "red")


    #Guardar perfil de parámetros
    def guardar_perfil(self):
        nombre_v3 = self._nombre_v3.get().strip()
        if not nombre_v3:
            messagebox.showerror("Error", "El nombre del perfil no puede estar vacío.")
            return

        # Validar datos
        corriente_fija_v3 = self._corriente_fija_v3.get().strip()
        saturacion_campo_v3 = self._saturacion_campo_v3.get().strip()
        tiempo_entre_mediciones_v3 = self._tiempo_entre_mediciones_v3.get().strip()
        intervalos_campos_v3 = self._pasos_v3.get().strip()

        if not all([corriente_fija_v3, saturacion_campo_v3, tiempo_entre_mediciones_v3, intervalos_campos_v3]):
            messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return

        # Guardar parámetros
        self.perfiles_ventana3[nombre_v3] = {
            "corriente_fija_v3": corriente_fija_v3,
            "saturacion_campo_v3": saturacion_campo_v3,
            "tiempo_entre_mediciones_v3": tiempo_entre_mediciones_v3,
            "intervalos_campos_v3": intervalos_campos_v3
        }

        guardar = validar_perfil_v3(nombre_v3, corriente_fija_v3, saturacion_campo_v3, tiempo_entre_mediciones_v3, intervalos_campos_v3)
        if guardar:
            self.guardar_perfiles_a_archivo()
            self.actualizar_combo_perfiles()
            messagebox.showinfo("Información", f"Perfil '{nombre_v3}' guardado exitosamente.")
        
    #Cargar perfil de parámetros
    def cargar_perfil(self):
        nombre_v3 = self.combo_perfiles.get()
        if nombre_v3 in self.perfiles_ventana3:
            perfil = self.perfiles_ventana3[nombre_v3]
            self._nombre_v3.set(nombre_v3)
            self._corriente_fija_v3.set(perfil["corriente_fija_v3"])
            self._saturacion_campo_v3.set(perfil["saturacion_campo_v3"])
            self._tiempo_entre_mediciones_v3.set(perfil["tiempo_entre_mediciones_v3"])
            self._pasos_v3.set(perfil["intervalos_campos_v3"])
            messagebox.showinfo("Información", f"Perfil '{nombre_v3}' cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfil válido para cargar.")

    #Actualizar los parámetros en el ComboBox
    def actualizar_parametros(self, event):
        self.cargar_perfil()

    #Actualizar Combobox
    def actualizar_combo_perfiles(self):
        self.combo_perfiles['values'] = list(self.perfiles_ventana3.keys())
    
    #Cargar Perfil en archivo
    def cargar_perfiles_desde_archivo(self):
        try:
            with open("perfiles_ventana3.json", "r") as archivo:
                datos = json.load(archivo)
                # Validar que todos los perfiles tengan las claves necesarias
                for nombre, perfil in datos.items():
                    if not all(key in perfil for key in ['corriente_fija_v3', 'saturacion_campo_v3', 'tiempo_entre_mediciones_v3']):
                        raise KeyError(f"El perfil '{nombre}' no tiene la estructura correcta.")
                return datos
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return {}
        except KeyError as e:
            messagebox.showerror('Error', f'Error al cargar los perfiles: {str(e)}')
            return {}

    #Guardar Perfil en archivo    
    def guardar_perfiles_a_archivo(self):
        with open("perfiles_ventana3.json", "w") as archivo:
            json.dump(self.perfiles_ventana3, archivo, indent=4)

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
        # Aplicar Configuración default de relés antes de cerrar la ventana
        self.encender_todos_reles()
        self.menu.withdraw()
        self.ventana_principal.deiconify()



    def volts_a_gauss(self, volts, probe_type):
        voltajes_mV = volts * 1000  # Convertir a milivoltios

        if probe_type == 'ST':
            gauss = voltajes_mV / 0.1  # Para HS Probe
        else:
            raise ValueError("Tipo de sonda no reconocido")
        return gauss
    
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
            # Validación e inicialización
            if verificar_inputs_gauss(
                self._saturacion_campo_v3.get(),
                self._corriente_fija_v3.get(),
                self._pasos_v3.get(),
                self._tiempo_entre_mediciones_v3.get(),
                self.menu,
            ):
                start_current = float(self._corriente_fija_v3.get())
                start_saturation = int(self._saturacion_campo_v3.get())
                step_size = int(self._pasos_v3.get())
                delay = float(self._tiempo_entre_mediciones_v3.get())
                self.fields = np.linspace(start_saturation, -start_saturation, num=step_size)
                self.array_prom_gauss_volts = []

                # Obtener configuración actual de los relés
                estado_configuracion_actual = [var.get() for var in self.relay_states]

                # Inicializar relés a "todos apagados"
                self.cambiar_estado_reles([False] * len(relay_pins))

                # Conexión y medición
                addresses = ["9", "6"]
                if verificar_dispositivo(addresses, self.menu, True):
                    try:
                        self.rm = pyvisa.ResourceManager()
                        multimetro = self.rm.open_resource('GPIB0::9::INSTR')
                        fuente = self.rm.open_resource('GPIB0::6::INSTR')
                        self.configurar_multimetro(multimetro, start_current)
                        self.configurar_fuente(fuente)

                        # Apagar la salida del multímetro al iniciar
                        multimetro.write("OUTPUT OFF")
                        self.mostrar_mensaje_inicio()

                        # Bucle principal de medición
                        for field in self.fields:
                            if self.detener_medicion:
                                break
                            for estados_reles in [[True, True, True, True], estado_configuracion_actual]:
 
                                if self.detener_medicion:
                                    break
                                
                                # Cambiar el estado de los relés
                                self.cambiar_estado_reles(estados_reles)
                                deltaV = self.calcular_deltaV(field)
                                fuente.write(f'SOUR:VOLT {deltaV}')
                                time.sleep(delay)

                                # Realizar medición
                                V = self.medir_voltaje(multimetro)

                                gauss = self.obtener_gauss()

                                # Almacenar los resultados
                                self.array_prom_gauss_volts.append((start_current, V, deltaV, gauss, field))
                                print(f"Field: {field}, Relés: {estados_reles}, V: {V}, Gauss: {gauss}")

                        # Actualizar la interfaz después de completar la medición
                        self.menu.after(0, self.boton_cerrar.config, {'state': tk.NORMAL})

                        if not(self.detener_medicion):
                            self.actualizar_interfaz_despues_de_medir()

                        # Apagar la fuente al finalizar
                        fuente.write("OUTP OFF")
                        self.detener_medicion = False

                    except pyvisa.errors.VisaIOError as e:
                        messagebox.showerror("Error de VISA", str(e), parent=self.menu)
                    finally:
                        if 'fuente' in locals():
                            fuente.close()
                        if 'multimetro' in locals():
                            multimetro.close()
                        self.detener_medicion = False
                else:
                    return

        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar_medicion)
        self.hilo_medicion.start()



    def cambiar_estado_reles(self, estados):
        """
        Cambia el estado de múltiples relevadores.
        """
        try:
            # Convertir a lista si `estados` es un solo booleano
            if isinstance(estados, bool):
                estados = [estados] * len(relay_pins)

            # Verificar longitud de la lista
            if len(estados) != len(relay_pins):
                raise ValueError(f"Se esperaba una lista con {len(relay_pins)} valores, pero se recibió: {estados}")

            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan(",".join(relay_pins), line_grouping=LineGrouping.CHAN_PER_LINE)
                task.write(estados, auto_start=True)  # Escribe un valor para cada canal
            time.sleep(0.5)

            estado_reles_str = ", ".join([f"Relé {i+1}: {'True' if estado else 'False'}" for i, estado in enumerate(estados)])
            print(f"Estado actual de los relés: {estado_reles_str}")

        except Exception as e:
            self.mostrar_estado(f"Error al cambiar el estado de los relés: {e}", "red")




    def encender_todos_reles(self):
        """
        Apagar todos los relés.
        """
        try:
            self.cambiar_estado_reles([True] * len(relay_pins))
            self.actualizar_checkboxes([True] * len(relay_pins))  # Sincronizar checkboxes
            self.mostrar_estado("Todos los relés Apagados.", "green")  # Añadir color
        except Exception as e:
            self.mostrar_estado(f"Error al Apagar los relés: {e}", "red")

    def apagar_todos_reles(self):
        """
        Encender todos los relés.
        """
        try:
            self.cambiar_estado_reles([False] * len(relay_pins))
            self.actualizar_checkboxes([False] * len(relay_pins))  # Sincronizar checkboxes
            self.mostrar_estado("Todos los relés Encendidos.", "blue")  # Añadir color
        except Exception as e:
            self.mostrar_estado(f"Error al Encender los relés: {e}", "red")

    def aplicar_configuracion(self, nuevos_estados, descripcion):
        """
        Aplica una configuración predefinida de relés.
        """
        try:
            if not isinstance(nuevos_estados, list):
                nuevos_estados = list(nuevos_estados)

            if len(nuevos_estados) != len(relay_pins):
                raise ValueError(f"La configuración debe contener {len(relay_pins)} estados.")

            self.cambiar_estado_reles(nuevos_estados)
            self.actualizar_checkboxes(nuevos_estados)

            # Guardar la descripción de la configuración aplicada
            self.descripcion_configuracion = descripcion

            self.mostrar_estado(f"Configuración {descripcion}", "green")
        except Exception as e:
            self.mostrar_estado(f"Error aplicando la configuración: {e}", "red")




    def calcular_deltaV(self, field):
        a,b = self.cargar_ecuacion_del_dia()
        deltaV = (field-b)/a
        deltaV = round(deltaV, 1) 
        return deltaV

    def guardar_prueba(self, event=None):
        if not (isinstance(self.array_prom_gauss_volts, np.ndarray) and self.array_prom_gauss_volts.size > 0 and not np.all(self.array_prom_gauss_volts == 0)) and self.array_prom_gauss_volts:
            # Obtener el título actual de la ventana como sugerencia de nombre
            proyecto_titulo = "test_gauss_"
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], initialfile=proyecto_titulo)
            m, b = self.cargar_ecuacion_del_dia()
            
            # Determinar la configuración aplicada
            configuracion_rele = ""
            if hasattr(self, 'descripcion_configuracion') and self.descripcion_configuracion:  # Configuración predefinida
                configuracion_rele = f"Configuración Relé: {self.descripcion_configuracion}"
            else:  # Configuración manual
                estados_reles = [f"{'T' if estado else 'F'}" for estado in self.obtener_estado_actual_reles()]
                configuracion_rele = f"Configuración Relé: {', '.join(estados_reles)}"
            
            if file_path:  # Si el usuario no cancela la selección del archivo
                with open(file_path, 'w') as file:
                    # Escribir encabezado con los datos de configuración y ecuación
                    file.write(f"Ecuación: {m:.6f}x {b:.6f}, Saturación de campo: {self._saturacion_campo_v3.get()}, ")
                    file.write(f"Tiempo entre mediciones: {self._tiempo_entre_mediciones_v3.get()}, Pasos: {self._pasos_v3.get()}\n")
                    file.write(f"{configuracion_rele}\n\n")
                    
                    # Escribir encabezados de columnas
                    file.write("Corriente Fija\t\tMedida Voltaje (Desactivado)\t\tR (Desactivado)\t\tDelta V (Desactivado)\t\tGauss Teórico (Desactivado)\t\tGauss Real (Desactivado)\t\t")
                    file.write("Medida Voltaje (Activado)\t\tR (Activado)\t\tDelta V (Activado)\t\tGauss Teórico (Activado)\t\tGauss Real (Activado)\n")
                    
                    # Escribir los datos en filas
                    for i in range(0, len(self.array_prom_gauss_volts), 2):  # Avanzar de dos en dos (pares: desactivado, activado)
                        desactivado = self.array_prom_gauss_volts[i]
                        activado = self.array_prom_gauss_volts[i + 1]
                        # Escribir una sola vez la corriente fija
                        file.write(f"{desactivado[0]:.6f}\t\t{desactivado[1]:.6f}\t\t{(desactivado[1]/desactivado[0]):.6f}\t\t"
                                f"{desactivado[2]:.6f}\t\t{desactivado[4]:.6f}\t\t{desactivado[3]:.6f}\t\t")
                        file.write(f"{activado[1]:.6f}\t\t{(activado[1]/activado[0]):.6f}\t\t{activado[2]:.6f}\t\t"
                                f"{activado[4]:.6f}\t\t{activado[3]:.6f}\n")
                    
                    # Mensaje de confirmación
                    messagebox.showinfo("Información", f"Datos guardados en: {file_path}")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para guardar. Realiza la medición primero.")

 

    def actualizar_interfaz_despues_de_medir(self):
        self.menu.after(0, self.mostrar_grafico(), "Información", "Medición completada")
    
    def mostrar_estado(self, mensaje, color="green"):
        """
        Muestra un mensaje de estado en la ventana de control de relés, si existe.
        """
        try:
            if self.ventana_reles is not None and self.texto_estado.winfo_exists():
                self.texto_estado.config(text=mensaje, fg=color)
        except AttributeError:
            print(f"Error mostrando estado: No se ha inicializado la ventana de relés.")
        except Exception as e:
            print(f"Error mostrando estado: {e}")  # Manejar otros errores

    def calcular_resistencia(self):
        # Inicializar las listas para los resultados
        resistencia_promedio_array = []
        saturacion_array = []
        try:
            # Iterar de dos en dos sobre los datos (pares: desactivado, activado)
            for i in range(0, len(self.array_prom_gauss_volts), 2):
                desactivado = self.array_prom_gauss_volts[i]
                activado = self.array_prom_gauss_volts[i + 1]
                
                # Desactivar y activar los datos de corriente y voltaje
                current1 = desactivado[0]
                voltaje1 = desactivado[1]
                current2 = activado[0]
                voltaje2 = activado[1]
                
                # Calcular las resistencias de cada estado
                r1 = voltaje1 / current1
                r2 = voltaje2 / current2
                
                # Calcular la resistencia promedio
                resistencia_promedio = (r1 + r2) / 2
                
                # Agregar los resultados a las listas correspondientes
                resistencia_promedio_array.append(resistencia_promedio)
                saturacion_array.append(desactivado[3])
        except Exception as e:
            print(e)
            return 1,1
            # Retornar las listas con los resultados calculados
        return resistencia_promedio_array, saturacion_array

    def mostrar_mensaje(self, titulo, mensaje):
        # Muestra un mensaje en el hilo principal
        messagebox.showinfo(titulo, mensaje)
        # Muestra el gráfico en el hilo principal
        self.mostrar_grafico()

    def mostrar_grafico(self):
        try:
            # Intentar obtener los datos para graficar
            resistencia_promedio, saturacion = self.calcular_resistencia()
            
            # Verificar que ambas listas tengan la misma longitud
            if len(resistencia_promedio) != len(saturacion):
                raise ValueError("La longitud de resistencia_promedio y saturacion no coincide")
            
            # Imprimir los datos para depuración
            
            # Graficar los datos experimentales
            self.ax.plot(saturacion, resistencia_promedio, marker='o', linestyle='-', label='Datos Experimentales')

            # Ajuste de una línea de tendencia si es necesario
            grado = 1  # Ajuste lineal
            

            coeficientes = np.polyfit(saturacion, resistencia_promedio, grado)
            tendencia = np.polyval(coeficientes, saturacion)
            self._R = 1 / coeficientes[0]  # Si deseas calcular la resistencia a partir del coeficiente

            if self.LineaTendencia_v3.get():  # Si la opción para la línea de tendencia está activada
                self.ax.plot(saturacion, tendencia, '--', label=f'Tendencia Lineal (R = {self._R:.4f} ohms)')
            
            # Mostrar la leyenda si es necesario
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend()
            
            # Ajustar límites del gráfico según los datos
            self.ax.set_xlim(min(saturacion) - 20, max(saturacion) + 20)
            self.ax.set_ylim(min(resistencia_promedio) - 100, max(resistencia_promedio) + 100)

            # Mostrar la grilla
            self.ax.grid(True)

            # Dibujar el gráfico en el canvas
            self.canvas.draw()

        except ValueError as e:
            # Mostrar un mensaje de error si los datos no son válidos
            messagebox.showerror("Error:", f"self.array_prom_gauss_volts no tiene el formato esperado\n{e}", parent=self.menu)
            return

    def borrar_grafico(self):
                # Agregar un marco para contener el gráfico y la barra de herramientas
        self.ax.grid(True)

        self.ax.clear()  # Limpiar el eje actual
        self.ax.set_title('Gráfico')
        self.ax.set_ylabel('R')
        self.ax.set_xlabel('G')
        plt.xlim(-6000, 6000)
        plt.ylim(-20, 20)
                # Mostrar la leyenda solo si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:  # Solo mostrar la leyenda si hay etiquetas
            self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()
    