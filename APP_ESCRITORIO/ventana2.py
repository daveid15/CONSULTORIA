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
from tkinter import messagebox
import nidaqmx
from nidaqmx.constants import LineGrouping



relay_pins = ['Dev2/port0/line0', 'Dev2/port0/line1', 'Dev2/port0/line2', 'Dev2/port0/line3']

configuraciones = [
    ((True, False, False, True), "Configuración 1","A-D (corriente) B-C (medición)"),
    ((True, False, True, False), "Configuración 2","A-C (corriente) B-D (medición)"),
    ((False, True, False, True), "Configuración 3","B-D (corriente) A-C (medición)"),
    ((False, True, True, False), "Configuración 4","B-C (corriente) A-D (medición)")
]

class Ventana2:
    #Constructor
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')
        bottonFont = ('Bold Italic', 10)

        #Variables
        self._nombre = tk.StringVar()
        self._corriente_fija = tk.StringVar()
        self._saturacion_campo = tk.StringVar()
        self._tiempo_entre_mediciones = tk.StringVar()
        self.LineaTendencia = tk.BooleanVar()

        #Lista para perfiles de parámetros
        self.perfiles_parametros = self.cargar_perfiles_desde_archivo()

        #Estados Configuraciones relés
        self.estados_reles = {}
        self.ventana_config_reles = None
        

        #Diseño ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title("Caracterización Electromagnética")
        self.menu.geometry("1000x720+0+0")

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Eléctrica', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
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

        #Botones
        btn_volver = tk.Button(self.menu, text="volver", bg="#99A8EF", command=self.volver)
        btn_volver.place(x=50, y=1.5)
        btn_guardar_perfil = tk.Button(self.menu, text="Guardar Perfil", command=self.guardar_perfil)
        btn_guardar_perfil.place(x=35, y=375)
        btn_cargar_perfil = tk.Button(self.menu, text="Cargar Perfil", command=self.cargar_perfil)
        btn_cargar_perfil.place(x=135, y=375)
        """OJITO Botón iniciar no esta asociado"""
        btn_iniciar = tk.Button(self.menu, text="Iniciar")
        btn_iniciar.place(x=100, y=420)
        btn_guardar_prueba = tk.Button(self.menu, text="Guardar Prueba", command=self.guardar_prueba)
        btn_guardar_prueba.place(x=75, y=465)
        self.btn_clear_plot = tk.Button(self.menu, text="Borrar Gráfico", command=self.borrar_grafico)
        self.btn_clear_plot.place(x=80, y=510)
        tk.Checkbutton(self.menu, text="Línea de Tendencia", variable=self.LineaTendencia).place(x=50, y=330)
        btn_config_reles = tk.Button(self.menu, text="Configurar Relés", command=self.abrir_ventana_configuracion_reles)
        btn_config_reles.place(x=80, y=555)


        # ComboBox para seleccionar perfiles de parámetros
        tk.Label(self.menu, text="Perfiles de Parámetros Guardados", bg="#A6C3FF").place(x=25, y=265)
        self.combo_perfiles = ttk.Combobox(self.menu, state="readonly")
        self.combo_perfiles.place(x=25, y=285, width=200)
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
        self.ax.set_title('Gráfico IV')
        self.ax.set_xlabel('Voltaje (V)')
        self.ax.set_ylabel('Corriente (A)')
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
        self.corrientes = None

        #Actualizar Perfiles
        self.cargar_perfiles_desde_archivo()
        self.actualizar_combo_perfiles()


        self.estados_reles = {pin: False for pin in relay_pins}  # False significa que el relé está apagado

        self.apagar_todos_reles()

    #Guardar perfil de parámetros
    def guardar_perfil(self):
        nombre = self._nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del perfil no puede estar vacío.")
            return
        
        if nombre in self.perfiles_parametros:
            messagebox.showerror("Error", "El nombre del perfil ya existe. Por favor elige otro nombre.")
            return

        #Validar que los valores sean correctos
        corriente_fija = self._corriente_fija.get().strip()
        saturacion_campo = self._saturacion_campo.get().strip()
        tiempo_entre_mediciones = self._tiempo_entre_mediciones.get().strip()

        if not corriente_fija or not saturacion_campo or not tiempo_entre_mediciones:
            messagebox.showerror("Error", "Todos los campos deben ser completados.")
            return
        
        #Guardar parámetros en el diccionario
        self.perfiles_parametros[nombre] = {
            "ventana": "Caracterización Electromagnética",
            "corriente_fija": corriente_fija,
            "saturacion_campo": saturacion_campo,
            "tiempo_entre_mediciones": tiempo_entre_mediciones
        }

        self.guardar_perfiles_a_archivo()

        #Actualizar el ComboBox con los perfiles guardados
        self.actualizar_combo_perfiles()
        messagebox.showinfo("Información", f"Perfil '{nombre}' guardado exitosamente.")



    #Cargar perfil de parámetros
    def cargar_perfil(self):
        nombre = self.combo_perfiles.get()
        perfil = self.perfiles_parametros.get(nombre)
        if perfil and perfil.get("ventana") == "Caracterización Electromagnética":
            self._nombre.set(nombre)
            self._corriente_fija.set(perfil["corriente_fija"])
            self._saturacion_campo.set(perfil["saturacion_campo"])
            self._tiempo_entre_mediciones.set(perfil["tiempo_entre_mediciones"])
            messagebox.showinfo("Información", f"Perfil '{nombre}' cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfil válido para cargar.")



    #Actualizar los parámetros en el ComboBox
    def actualizar_parametros(self, event):
        self.cargar_perfil()



    #Actualizar Combobox
    def actualizar_combo_perfiles(self):
        perfiles_filtrados = {k: v for k, v in self.perfiles_parametros.items() if v.get("ventana") == "Caracterización Electromagnética"}
        self.combo_perfiles['values'] = list(perfiles_filtrados.keys())

    

    #Cargar Perfil en archivo
    def cargar_perfiles_desde_archivo(self):
        try:
            with open("perfiles_parametros.json", "r") as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}



    #Guardar Perfil en archivo    
    def guardar_perfiles_a_archivo(self):
        with open("perfiles_parametros.json", "w") as archivo:
            json.dump(self.perfiles_parametros, archivo, indent=4)



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

    

    def aplicar_configuracion(self, configuracion):
        self.cambiar_configuracion(configuracion)
        messagebox.showinfo("Éxito", "Configuración aplicada.")
        

    def cambiar_configuracion(self,configuracion):
        for index, pin in enumerate(relay_pins):
            estado_actual = self.estados_reles[pin]
            if configuracion[index] != estado_actual:
                try:
                    with nidaqmx.Task() as task:
                        # Añadir el canal de salida digital
                        task.do_channels.add_do_chan(pin, line_grouping=LineGrouping.CHAN_PER_LINE)
                        # Escribir el estado (True para HIGH, False para LOW)
                        task.write(configuracion[index])
                        self.estados_reles[pin] = configuracion[index]
                        # Añadir un retardo para que los cambios tengan tiempo para ser aplicados
                        time.sleep(0.5)
                        
                except nidaqmx.errors.DaqError as e:
                    messagebox.showerror("Error de DAQ", str(e))


    def encender_todos_reles(self):
        try:
            for pin in relay_pins:
                with nidaqmx.Task() as task:
                    task.do_channels.add_do_chan(pin, line_grouping=LineGrouping.CHAN_PER_LINE)
                    task.write(True)  # Encender (HIGH)
                    self.estados_reles[pin] = True
                    time.sleep(0.5)  # Retardo para asegurar que el cambio se aplique
            messagebox.showinfo("Éxito", "Todos los relés encendidos.")
        except nidaqmx.errors.DaqError as e:
            messagebox.showerror("Error de DAQ", str(e))

    def apagar_todos_reles(self):
        try:
            for pin in relay_pins:
                with nidaqmx.Task() as task:
                    task.do_channels.add_do_chan(pin, line_grouping=LineGrouping.CHAN_PER_LINE)
                    task.write(False)  # Apagar (LOW)
                    self.estados_reles[pin] = False
                    time.sleep(0.5)  # Retardo para asegurar que el cambio se aplique
            messagebox.showinfo("Éxito", "Todos los relés apagados.")
        except nidaqmx.errors.DaqError as e:
            messagebox.showerror("Error de DAQ", str(e))

    #Ventana Configuraciones Reles
    def abrir_ventana_configuracion_reles(self):
        if self.ventana_config_reles is None or not self.ventana_config_reles.winfo_exists():
            # Crear la ventana de configuraciones de relés
            self.ventana_config_reles = tk.Toplevel(self.menu)
            self.ventana_config_reles.title("Configuraciones de Relés")
            self.ventana_config_reles.geometry("400x250+0+0")

            config_frame = tk.LabelFrame(self.ventana_config_reles, text="Configuraciones de Relés", padx=10, pady=10)
            config_frame.pack(fill="both", expand=True)

            for i, (config, label, description) in enumerate(configuraciones):
                lbl = tk.Label(config_frame, text=description)
                lbl.grid(row=i, column=0, sticky='w')
                btn = tk.Button(config_frame, text=label, command=lambda config=config: self.aplicar_configuracion(config))
                btn.grid(row=i, column=1, padx=5, pady=5)

            # Botón para encender todos los relés
            btn_encender_todos = tk.Button(config_frame, text="Encender Todos los Relés", command=self.encender_todos_reles)
            btn_encender_todos.grid(row=len(configuraciones), column=0, padx=5, pady=10, sticky='w')

            # Botón para apagar todos los relés
            btn_apagar_todos = tk.Button(config_frame, text="Apagar Todos los Relés", command=self.apagar_todos_reles)
            btn_apagar_todos.grid(row=len(configuraciones), column=1, padx=5, pady=10, sticky='e')

            # Asegurar que la referencia a la ventana se elimine cuando esta se cierre
            self.ventana_config_reles.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_configuracion_reles)

    #Evitar ventana configuracion reles duplicada
    def cerrar_ventana_configuracion_reles(self):
        if self.ventana_config_reles is not None:
            self.ventana_config_reles.destroy()
        self.ventana_config_reles = None





    def iniciar(self):
        print("Iniciado")
        


    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()



    def guardar_prueba(self, event=None):  #Accept the event argument from Tkinter
        
        if self.corrientes is not None and self.resultados is not None:
            # Obtener el título actual de la ventana como sugerencia de nombre
            proyecto_titulo = "test_"

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")],initialfile=proyecto_titulo)

            if file_path:  # Si el usuario no cancela la selección del archivo
                with open(file_path, 'w') as file:
                    file.write("Corriente (A)\tVoltaje (V)\n\n")
                    #
                    for corriente, voltaje in self.resultados:
                        file.write(f"{corriente:.3f}\t\t{voltaje}\n")
                messagebox.showinfo("Información", f"Datos guardados en: {file_path}")
            else:
                print("Guardado cancelado.")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para guardar. Realiza la medición primero.")



    def borrar_grafico(self):
        self.ax.set_title('Gráfico IV')
        self.ax.clear()  # Limpiar el eje actual
        self.ax.set_ylabel('Corriente (A)')
        self.ax.set_xlabel('Voltaje (V)')
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()


