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
import requests

class Ventana1:
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')

        #Variables
        self._nombre = tk.StringVar()
        self._R = tk.StringVar()
        self._intervalo_simetrico = tk.StringVar()
        self._intervalos_corriente = tk.StringVar()
        self._tiempo_entre_mediciones = tk.StringVar()
        self.LineaTendencia = tk.BooleanVar()
        # Variable de control para el hilo
        self.detener_medicion = False
        self.resultados =[]
        # Lista para perfiles de parámetros
        self.perfiles_parametros = self.cargar_perfiles_desde_archivo()

        #Diseño Ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title('Caracterización Eléctrica')
        widht_menu =1000
        height_menu = 600
        centrar_ventana(self.menu,widht_menu,height_menu )

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Eléctrica', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.menu, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)
        
        #Botones
        btn_volver = tk.Button(self.menu, text="volver", bg="#99A8EF", command=self.volver)
        btn_volver.place(x=50, y=1.5)

        tk.Checkbutton(self.menu, text="Línea de Tendencia", variable=self.LineaTendencia).place(x=50, y=330)

        btn_guardar_perfil = tk.Button(self.menu, text="Guardar Perfil", command=self.guardar_perfil)
        btn_guardar_perfil.place(x=35, y=375)

        btn_cargar_perfil = tk.Button(self.menu, text="Cargar Perfil", command=self.cargar_perfil)
        btn_cargar_perfil.place(x=135, y=375)

        btn_iniciar = tk.Button(self.menu, text="Iniciar", command=self.medir_IV_curve)
        btn_iniciar.place(x=100, y=420)

        btn_guardar_prueba = tk.Button(self.menu, text="Guardar Prueba", command=self.guardar_prueba)
        btn_guardar_prueba.place(x=75, y=465)

        self.btn_clear_plot = tk.Button(self.menu, text="Borrar Gráfico", command=self.borrar_grafico)
        self.btn_clear_plot.place(x=80, y=510)


        # ComboBox para seleccionar perfiles de parámetros
        tk.Label(self.menu, text="Perfiles de Parámetros Guardados", bg="#A6C3FF").place(x=25, y=265)
        self.combo_perfiles = tk.ttk.Combobox(self.menu, state="readonly")
        self.combo_perfiles.place(x=25, y=285, width=200)
        self.combo_perfiles.bind("<<ComboboxSelected>>", self.actualizar_parametros)


        #Entradas
        tk.Label(self.menu, text="Nombre", bg="#A6C3FF").place(x=25, y=60)
        tk.Entry(self.menu, textvariable=self._nombre).place(x=25, y=80, width=210)

        tk.Label(self.menu, text="Intervalo Simétrico(A)", bg="#A6C3FF").place(x=25, y=110)
        tk.Entry(self.menu, textvariable=self._intervalo_simetrico).place(x=25, y=130, width=210)

        tk.Label(self.menu, text="Intervalos de Corriente", bg="#A6C3FF").place(x=25, y=160)
        tk.Entry(self.menu, textvariable=self._intervalos_corriente).place(x=25, y=180, width=210)

        tk.Label(self.menu, text="Tiempo entre Mediciones(s)", bg="#A6C3FF").place(x=25, y=210)
        tk.Entry(self.menu, textvariable=self._tiempo_entre_mediciones).place(x=25, y=230, width=210)

        # Fecha
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        etiqueta_fecha = tk.Label(self.menu, text=f"Fecha: {fecha_actual}", font=("Arial", 10))
        etiqueta_fecha.place(x=800, y=5)
        
        self.frame_plot = tk.Frame(self.menu)
        self.frame_plot.place(x=300, y=50, width=700, height=500)

        # Configurar la figura de Matplotlib y el eje
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title('Gráfico IV')
        self.ax.set_xlabel('Corriente (A)')
        self.ax.set_ylabel('Voltaje (V)')
        self.ax.grid(True)


        # Crear un lienzo de Tkinter para la figura
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Agregar la barra de herramientas de navegación en la parte inferior
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)  # Mover la barra de herramientas abajo

        # Mostrar la leyenda solo si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:  # Solo mostrar la leyenda si hay etiquetas
            self.ax.legend()

        # Mantener el gráfico arriba
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        self.rm = None
        self.corrientes = None

        #Actualizar Perfiles
        self.cargar_perfiles_desde_archivo()
        self.actualizar_combo_perfiles()

    #Guardar perfil de parámetros
    def guardar_perfil(self):
        bandera = True
        nombre = self._nombre.get().strip()


        #Validar que los valores sean correctos
        intervalo_simetrico = self._intervalo_simetrico.get().strip()
        intervalos_corriente = self._intervalos_corriente.get().strip()
        tiempo_entre_mediciones = self._tiempo_entre_mediciones.get().strip()

        if not intervalo_simetrico or not intervalos_corriente or not tiempo_entre_mediciones:
            messagebox.showerror("Error", "Todos los campos deben ser completados.")
            bandera = False

        #Guardar parámetros en el diccionario
        self.perfiles_parametros[nombre] = {
            "intervalo_simetrico": intervalo_simetrico,
            "intervalos_corriente": intervalos_corriente,
            "tiempo_entre_mediciones": tiempo_entre_mediciones
        }
        guardar = validar_perfil_v1(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones)
        if guardar and bandera:
            self.guardar_perfiles_a_archivo()
            self.actualizar_combo_perfiles()
            messagebox.showinfo("Información", f"Perfil '{nombre}' guardado exitosamente.",parent = self.menu)

        #Actualizar el ComboBox con los perfiles guardados



    #Cargar perfil de parámetros
    def cargar_perfil(self):
        nombre = self.combo_perfiles.get()
        if nombre in self.perfiles_parametros:
            perfil = self.perfiles_parametros[nombre]
            self._nombre.set(nombre)
            self._intervalo_simetrico.set(perfil["intervalo_simetrico"])
            self._intervalos_corriente.set(perfil["intervalos_corriente"])
            self._tiempo_entre_mediciones.set(perfil["tiempo_entre_mediciones"])
            messagebox.showinfo("Información", f"Perfil '{nombre}' cargado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un perfil válido para cargar.")

    #Actualizar los parámetros en el ComboBox
    def actualizar_parametros(self, event):
        self.cargar_perfil()

    #Actualizar Combobox
    def actualizar_combo_perfiles(self):
        self.combo_perfiles['values'] = list(self.perfiles_parametros.keys())

    
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
    #s
    # Obtención de entradas
    @property
    def nombre(self):
        return self._nombre.get()

    @property
    def intervalo_simetrico(self):
        return self._intervalo_simetrico.get()

    @property
    def intervalos_corriente(self):
        return self._intervalos_corriente.get()

    @property
    def tiempo_entre_mediciones(self):
        return self._tiempo_entre_mediciones.get()
    @property
    def R(self):
        return self._R.get()
    
    #Funciones Botones

    def iniciar(self):
        print("Iniciado")



    # Volver al menú
    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()

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

        # Etiqueta con el mensaje
        mensaje_label = tk.Label(self.popup, text="¿Deseas detener la medición?", padx=10, pady=10)
        mensaje_label.pack()

        # Botón para cerrar la ventana y confirmar la detención
        self.boton_cerrar = tk.Button(self.popup, text="Cancelar", command=self.confirmar_detener_medicion)
        self.boton_cerrar.pack(pady=10)

        # Manejar el evento de cierre de la ventana emergente
        self.popup.protocol("WM_DELETE_WINDOW", self.confirmar_detener_medicion)

    def confirmar_detener_medicion(self):
        # Cambiar la variable de control para detener el hilo
        self.detener_medicion = True
        self.popup.destroy()  # Cerrar la ventana emergente

        
    def medir_IV_curve(self):
        def ejecutar_medicion():
            start_current_str = self._intervalo_simetrico.get()
            step_size_str = self._intervalos_corriente.get()
            delay_str = self._tiempo_entre_mediciones.get()

            # Validar que todos los valores sean válidos
            if verificar_inputs(start_current_str, step_size_str, delay_str, self.menu):
                # Continúa con el proceso si no hay errores
                start_current = float(start_current_str)
                step_size = int(step_size_str)
                delay = float(delay_str)
                self.corrientes = np.linspace(start_current, -start_current, num=step_size)
                self.resultados = []

                # Inicializar el gestor de recursos VISA
                self.rm = pyvisa.ResourceManager()

                # Abrir la conexión con el multímetro y realizar la medición
                addresses= ["9"]
                if verificar_dispositivo(addresses, self.menu, False):
                    try:
                        with self.rm.open_resource('GPIB0::9::INSTR') as multimetro:
                            self.mostrar_mensaje_inicio()
                            # Configurar el multímetro para ser una fuente de corriente y medir voltaje
                            multimetro.write("*RST")  # Resetear el equipo
                            multimetro.write(":SOUR:FUNC CURR")  # Configurar como fuente de corriente
                            multimetro.write("CONF:VOLT:DC")  # Configurar para medir voltaje
                            # Encender la salida
                            multimetro.write("OUTPUT ON")
                            
                            for corriente in self.corrientes:
                                try:
                                    self.detener_medicion = False  # Reiniciar la variable de control

                                    if self.detener_medicion:
                                        break
                                    # Aplicar la corriente
                                    multimetro.write(f":SOUR:CURR {corriente}")

                                    time.sleep(delay)

                                    # Medir el voltaje mientras se aplica la corriente
                                    medida_voltaje = multimetro.query(":MEAS:VOLT:DC?")
                                    valores = medida_voltaje.strip().split(',')
                                    
                                    V = float(valores[0])
                                    self.resultados.append((corriente, V))
                                    #print(f"{corriente}, {V}") calmao la bateria, igual en la ventana 1 no se usa el gauss ahyaa
                            

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
                            messagebox.showerror("'VI_ERROR_LIBRARY_NFOUND","Error: No se pudo localizar o cargar la biblioteca requerida por VISA. Verifique que los controladores VISA estén instalados correctamente y el software NI-VISA esté instalado." , parent=self.menu)
                        else:
                            messagebox.showerror("'Error inesperado de VISA",f"{e}" , parent=self.menu)
                else:
                    return
        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar_medicion)
        self.hilo_medicion.start()





    def actualizar_interfaz_despues_de_medir(self):
        self.confirmar_detener_medicion()
        self.menu.after(0, self.mostrar_grafico(), "Información", "Medición completada")
    
    def mostrar_mensaje(self, titulo, mensaje):
        # Muestra un mensaje en el hilo principal
        messagebox.showinfo(titulo, mensaje)
        
        # Muestra el gráfico en el hilo principal
        self.mostrar_grafico()
    
    def mostrar_grafico(self):
        try:
            corrientes, voltajes = zip(*self.resultados)
        except ValueError:
            print("Error: self.resultados no tiene el formato esperado.")
            return

        # Graficar los datos experimentales con una etiqueta
        self.ax.plot(corrientes, voltajes, marker='o', linestyle='-', label='Datos Experimentales')

        # Ajustar una línea de tendencia
        grado = 1
        coeficientes = np.polyfit(corrientes, voltajes, grado)
        resistencia = 1 / coeficientes[0]
        self._R=resistencia
        if self.LineaTendencia.get():
            # Calcular la línea de tendencia usando corrientes para el eje x
            tendencia = np.polyval(coeficientes, corrientes)
            self.ax.plot(corrientes, tendencia, '--', label=f'Tendencia Lineal (R = {resistencia:.4f} ohms)')

        # Configurar el título y las etiquetas de los ejes
        self.ax.set_title('Gráfico IV')
        self.ax.set_xlabel('Corriente (A)')
        self.ax.set_ylabel('Voltaje (V)')

        # Mostrar la leyenda solo si hay etiquetas definidas
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()
        else:
            print("No se encontraron artistas con etiquetas para la leyenda.")

        self.ax.grid(True)
        self.canvas.draw()
    
    def browse_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        self.entry_start.delete(0, tk.END)
        self.entry_end.delete(0, tk.END)
        self.entry_step.delete(0, tk.END)
        self.entry_start.insert(0, file_path)
    def verificar_servidor(self,url):
        try:
            # Hacer una solicitud GET al servidor
            response = requests.get(url)
            return True
        except:
            return False
        


    def guardar_prueba(self, event=None):
        if not (isinstance(self.corrientes, np.ndarray) and self.corrientes.size > 0 and not np.all(self.corrientes == 0)) and  self.resultados:
            # Obtener el título actual de la ventana como sugerencia de nombre
            proyecto_titulo = "test_"

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], initialfile=proyecto_titulo)

            if file_path:  # Si el usuario no cancela la selección del archivo
                with open(file_path, 'w') as file: 
                    file.write(f"fecha: {datetime.now().strftime('%d-%m-%Y')}\nIntervalo(A): {self._intervalo_simetrico.get()}, intervalos de corrientes(A): {self._intervalos_corriente.get()}, Tiempo entre mediciones(s): {self._tiempo_entre_mediciones.get()}\nR: \n")
                    file.write(f"Corriente (A),\tVoltaje (V), Resistencia (Ohm)\t\n\n")
                    mediciones=[]
                    for corriente, voltaje in self.resultados:
                        mediciones.append({"corriente":corriente, "voltaje":voltaje})
                        file.write(f"{corriente:.3f}\t\t{voltaje}\t\t{(voltaje/corriente):.6f}\n")
                
                messagebox.showinfo("Información", f"Datos guardados en: {file_path}")

                # Verificar si el servidor está activo antes de enviar los datos
                if self.verificar_servidor("http://127.0.0.1:8000"):
                    # Llamar a enviar_datos_prueba si el servidor está activo
                    self.enviar_datos_prueba(self._intervalos_corriente.get(), self._intervalo_simetrico.get(), proyecto_titulo, self._tiempo_entre_mediciones.get())
                else:
                    messagebox.showwarning("Advertencia", "El servidor no está disponible. No se enviarán los datos.")
                    
            else:
                print("Guardado cancelado.")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para guardar. Realiza la medición primero.")
    def borrar_grafico(self):
        # Limpiar el eje actual
        self.ax.clear()

        # Restablecer el título y etiquetas
        self.ax.set_title('Gráfico IV')
        self.ax.set_xlabel('Corriente (A)')
        self.ax.set_ylabel('Voltaje (V)')



        # Mostrar la leyenda solo si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:  # Solo mostrar la leyenda si hay etiquetas
            self.ax.legend()

        # Redibujar el gráfico en el lienzo
            # Reestablecer la cuadrícula
        self.ax.grid(True)
        self.canvas.draw()
    def enviar_datos_prueba(self,intervalo_corriente, intervalo_simetrico, nombre, tiempo_entre_mediciones):
            url = "http://127.0.0.1:8000/caracterizacion/api_parametro/"

            try:
                intervalo_simetrico = float(intervalo_simetrico)
                intervalo_corriente = float(intervalo_corriente)
            except ValueError as e:
                print(f"intervalo_simetrico: {intervalo_simetrico} (tipo: {type(intervalo_simetrico)})")
                print(f"intervalo_corriente: {intervalo_corriente} (tipo: {type(intervalo_corriente)})")

            #json
            data = {
                "perfil_parametro_name": nombre,
                "intervalo_simetrico": intervalo_simetrico,
                "intervalo_corriente": intervalo_corriente,
                "delay": tiempo_entre_mediciones,
                "bloqueado": False,
                "pruebas": [
                {
                    "prueba_name": nombre,
                    "tipo": "Electrica",
                    "mediciones": []
                },
            ]

        }
                

        # Generar mediciones según los intervalos
            for prueba in data["pruebas"]:  

                for corriente, voltaje in self.resultados:
                    
                    resistencia = round(voltaje / corriente, 6) if corriente != 0 else None
    

                    prueba["mediciones"].append({
                        "corriente": round(corriente, 6),
                        "voltaje": round(voltaje, 6),
                        "resistencia": resistencia,
                        "fecha": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                        "intervalo_corriente": intervalo_corriente,
                        "intervalo_simetrico": intervalo_simetrico,
                        "tiempo_entre_mediciones": tiempo_entre_mediciones

                })

            headers = {
                "Content-Type": "application/json",
            }        

            try:
                # Enviar el POST request con los datos
                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 201:
                    print("Perfil de Parámetro creado exitosamente!")
                    print(json.dumps(data, indent=4))
                    return response.json()
                else:
                    print(f"Error al crear el perfil: {response.status_code}")
                    print("Detalle:", response.text)
                    return None  # Retorna None en caso de error
                
            except requests.exceptions.RequestException as e:
                    print(f"Error en la conexión: {e}")
                    return None