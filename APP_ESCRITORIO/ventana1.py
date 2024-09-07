from tkinter import *
import tkinter as tk
from datetime import datetime
import numpy as np
import pyvisa
import time
import matplotlib.pyplot as plt
import threading
from validacion import *
class Ventana1:
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')
        bottonFont = ('Bold Italic', 10)

        #Variables
        self._nombre = tk.StringVar()
        self._intervalo_simetrico = tk.IntVar()
        self._intervalos_corriente = tk.IntVar()
        self._tiempo_entre_mediciones = tk.DoubleVar()
        self.LineaTendencia = tk.BooleanVar()

        #Diseño Ventana
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu = menu
        self.menu.title('Caracterización Eléctrica')
        self.menu.geometry('1000x600')

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.menu, text='Caracterización Eléctrica', font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.menu, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.menu, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Botones
        btn_volver = tk.Button(self.menu, text="volver a menu", command=self.volver)
        btn_volver.place(x=100, y=5)

        tk.Checkbutton(self.menu, text="Línea de Tendencia", variable=self.LineaTendencia).place(x=25, y=300)

        btn_guardar_seccion = tk.Button(self.menu, text="Guardar Sección", command=self.guardar_seccion)
        btn_guardar_seccion.place(x=25, y=350)

        btn_iniciar = tk.Button(self.menu, text="Iniciar", command=self.medir_IV_curve)
        btn_iniciar.place(x=25, y=400)

        btn_guardar_prueba = tk.Button(self.menu, text="Guardar Prueba", command=self.guardar_prueba)
        btn_guardar_prueba.place(x=25, y=450)


        #Entradas
        tk.Label(self.menu, text="Nombre").place(x=25, y=50)
        tk.Entry(self.menu, textvariable=self._nombre).place(x=25, y=70, width=200)

        tk.Label(self.menu, text="Intervalo Simétrico").place(x=25, y=100)
        tk.Entry(self.menu, textvariable=self._intervalo_simetrico).place(x=25, y=120, width=200)

        tk.Label(self.menu, text="Intervalos de Corriente").place(x=25, y=150)
        tk.Entry(self.menu, textvariable=self._intervalos_corriente).place(x=25, y=170, width=200)

        tk.Label(self.menu, text="Tiempo entre Mediciones").place(x=25, y=200)
        tk.Entry(self.menu, textvariable=self._tiempo_entre_mediciones).place(x=25, y=220, width=200)

        # Fecha
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        etiqueta_fecha = tk.Label(self.menu, text=f"Fecha: {fecha_actual}", font=("Arial", 10))
        etiqueta_fecha.place(x=800, y=5)
        
        self.rm = None
        self.corrientes = None

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
    
    #Funciones Botones
    def guardar_seccion(self):
        print("Sección Guardada")

    def iniciar(self):
        print("Iniciado")

    def guardar_prueba(self):
        print("Prueba Guardada")

    # Volver al menú
    def volver(self):
        self.menu.withdraw()
        self.ventana_principal.deiconify()
        
        
    def medir_IV_curve(self):
        def ejecutar_medicion():
            rm = pyvisa.ResourceManager()
            print(self._intervalo_simetrico.get())
            # Obtener los valores de corriente desde los inputs del usuario
            start_current_str = self._intervalo_simetrico.get()
            step_size_str = self._intervalos_corriente.get()
            delay_str = self._tiempo_entre_mediciones.get()

            # Validar que todos los valores sean válidos
            if verificar_inputs(start_current_str, step_size_str, delay_str, self.menu):
                # Continúa con el proceso si no hay errores
                print("Todos los inputs son válidos. Continuar con el proceso...")
                start_current = float(start_current_str)
                step_size = int(step_size_str)
                delay = float(delay_str)
            else:
                # Se mostrarán los errores en una ventana emergente
                print("Hay errores en los inputs.")


            # Crear el rango de corrientes a medir
            self.corrientes = np.linspace(start_current, start_current*(-1), num=step_size)
            self.resultados = []

            # Abrir la conexión con el multímetro
            verificar_dispositivo("9", self.menu)

            multimetro = rm.open_resource('GPIB0::9::INSTR')  # Dirección GPIB

            # Realizar el barrido IV
            for corriente in self.corrientes:
                try:
                    # Configurar el multímetro para enviar corriente
                    multimetro.write(":SOUR:FUNC CURR")
                    multimetro.write(f":SOUR:CURR {corriente}")
                    time.sleep(delay)

                    # Configurar el multímetro para medir voltaje
                    multimetro.write("CONF:VOLT:DC")
                    time.sleep(delay)

                    # Medir el voltaje
                    medida_voltaje = multimetro.query("MEAS:VOLT:DC?")
                    self.resultados.append((corriente, float(medida_voltaje.strip())))
                    #self.actualizar_interfaz_despues_de_medir()

                except pyvisa.errors.VisaIOError as e:
                    print(f"Error de VISA: {e}")
                    self.resultados.append((corriente, None))

                except ValueError as e:
                    print(f"Error en los valores obtenidos: {e}")
                    self.resultados.append((corriente, None))

            multimetro.write("OUTPUT OFF")
            multimetro.close()

        # Ejecutar la medición en un hilo separado
        self.hilo_medicion = threading.Thread(target=ejecutar_medicion)
        self.hilo_medicion.start()
