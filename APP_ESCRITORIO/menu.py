from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from ventana1 import Ventana1
from ventana2 import Ventana2
from ventana3 import Ventana3
from ventana4 import Ventana4
import os            
from ventana4 import Ventana4
import os            
from validacion import centrar_ventana

class Menu:
    def __init__(self, main):
        global imagen_ruta

        labelFont = ("Bold Italic", 20, 'bold')
        someFont = ('Bold Italic', 15)
        bottonFont = ('Bold Italic', 10)

        self.main = main
        self.main.title('MENÚ PRINCIPAL')
        widht_main =1000
        height_main = 600
        centrar_ventana(self.main,widht_main,height_main )
        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.main, text="MENÚ PRINCIPAL", font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.main, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.main, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)




        #Botones
        boton1=tk.Button(left_frame, text='Caracterización Eléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana1)
        boton1.place(relx=0.13, rely=0.1)
        boton2=tk.Button(left_frame, text='Caracterización Magnetoeléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana2)
        boton2.place(relx=0.13, rely=0.3)
        boton3=tk.Button(left_frame, text='Caracterización Magnetoeléctrica \n Invertida',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana3)
        boton3.place(relx=0.13, rely=0.5)
    
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
    main.protocol("WM_DELETE_WINDOW")
    app = Menu(main)
    main.mainloop()