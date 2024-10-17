from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from ventana1 import Ventana1
from ventana2 import Ventana2
from ventana3 import Ventana3
from ventana4 import Ventana4            

class Menu:
    def __init__(self, main):
        global imagen_ruta

        labelFont = ("Bold Italic", 20, 'bold')
        someFont = ('Bold Italic', 15)
        bottonFont = ('Bold Italic', 10)

        self.main = main
        self.main.title('MENÚ PRINCIPAL')
        self.main.geometry('1000x600')

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.main, text="MENÚ PRINCIPAL", font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.main, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.main, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Imagenes
        self.imagen_fuente = "APP_ESCRITORIO/fotos/FuentePoder.png"
        imagen_fuente = Image.open(self.imagen_fuente)
        imagen_tk_fuente = ImageTk.PhotoImage(imagen_fuente)
        label_fuente = tk.Label(right_frame, image=imagen_tk_fuente, width=175, height=120)
        label_fuente.place(relx=0.315, rely=0.3)

        self.imagen_gaussmeter = "APP_ESCRITORIO/fotos/Gaussmeter.png"
        imagen_gaussmeter = Image.open(self.imagen_gaussmeter)
        imagen_tk_gaussmeter = ImageTk.PhotoImage(imagen_gaussmeter)
        label_gaussmeter = tk.Label(right_frame, image=imagen_tk_gaussmeter, width=175, height=120)
        label_gaussmeter.place(relx=0.5575, rely=0.3)

        self.imagen_multimetro = "APP_ESCRITORIO/fotos/Multimetro.png"
        imagen_multimetro = Image.open(self.imagen_multimetro)
        imagen_tk_multimetro = ImageTk.PhotoImage(imagen_multimetro)
        label_multimetro = tk.Label(right_frame, image=imagen_tk_multimetro, width=175, height=120)
        label_multimetro.place(relx=0.80, rely=0.3)

        #Nombres Instrumentos
        label_poder = tk.Label(right_frame, text='Fuente de Poder', font=someFont, bg="#D9D9D9")
        label_poder.place(relx=0.325, rely=0.23)
        label_gauss = tk.Label(right_frame, text='Gaussmeter', font=someFont, bg="#D9D9D9")
        label_gauss.place(relx=0.585, rely=0.23)
        label_multi = tk.Label(right_frame, text='Multimetro', font=someFont, bg="#D9D9D9")
        label_multi.place(relx=0.835, rely=0.23)

        #Botones
        boton1=tk.Button(left_frame, text='Caracterización Eléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana1)
        boton1.place(relx=0.13, rely=0.1)
        boton2=tk.Button(left_frame, text='Caracterización Magnetoeléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana2)
        boton2.place(relx=0.13, rely=0.3)
        boton3=tk.Button(left_frame, text='Caracterización Magnetoeléctrica \n Invertida',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana3)
        boton3.place(relx=0.13, rely=0.5)
        boton4=tk.Button(left_frame, text='Pruebas',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana4)
        boton4.place(relx=0.13, rely=0.7)
    
    def abrir_ventana1(self):
        self.main.withdraw()
        nueva_ventana = tk.Toplevel(self.main)
        Ventana1(nueva_ventana, self.main)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def abrir_ventana2(self):
        self.main.withdraw()
        nueva_ventana = tk.Toplevel(self.main)
        Ventana2(nueva_ventana, self.main)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def abrir_ventana3(self):
        self.main.withdraw()
        nueva_ventana = tk.Toplevel(self.main)
        Ventana3(nueva_ventana, self.main)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
    def abrir_ventana4(self):
        self.main.withdraw()
        nueva_ventana = tk.Toplevel(self.main)
        Ventana4(nueva_ventana, self.main)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        self.main.quit() 
        self.main.destroy()
    
if __name__ == "__main__":
    main= tk.Tk()
    imagen = tk.PhotoImage("APP_ESCRITORIO\fotos\complaint-exist.png")
    app = Menu(main)
    main.mainloop()