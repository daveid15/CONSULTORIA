from tkinter import *
import tkinter as tk
from ventana1 import Ventana1
from ventana2 import Ventana2
from ventana3 import Ventana3
from ventana4 import Ventana4            

class Menu:
    def __init__(self, main):
        labelFont = ("Bold Italic", 20, 'bold')
        bottonFont = ('Bold Italic', 10)

        self.main = main
        self.main.title('MENÚ PRINCIPAL')
        self.main.geometry('1000x600')

        #Pantalla con sus colores y titulo respectivo
        tk.Label(self.main, text="MENÚ PRICIPAL", font=labelFont, bg='#D9D9D9').pack(side=TOP, fill=X)
        right_frame = tk.Frame(self.main, bg="#1F6095")
        right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
        left_frame = tk.Frame(self.main, bg="#A6C3FF")
        left_frame.place(x=10, y=45, relheight=0.90, relwidth=0.275)

        #Botones
        boton1=tk.Button(left_frame, text='Caracterización Eléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana1)
        boton1.place(relx=0.13, rely=0.1)
        boton2=tk.Button(left_frame, text='Caracterización Magnetoeléctrica',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana2)
        boton2.place(relx=0.13, rely=0.3)
        boton3=tk.Button(left_frame, text='Caracterización Magnetoeléctrica Invertida',bg="#FDFDFD", font=bottonFont, width=24, height=4, command=self.abrir_ventana3)
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
        self.menu.quit() 
        self.menu.destroy()
    
if __name__ == "__main__":
    main= tk.Tk()
    app = Menu(main)
    main.mainloop()