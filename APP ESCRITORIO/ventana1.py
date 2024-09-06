from tkinter import *
import tkinter as tk

class Ventana1:
    def __init__(self, menu, ventana_principal):
        labelFont = ("Bold Italic", 20, 'bold')
        bottonFont = ('Bold Italic', 10)

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
        btn_volver = tk.Button(self.menu, font=bottonFont, text="volver a menu", command=self.volver)
        btn_volver.place(x=100, y=100)

    def volver(self):
        self.menu.withdraw()  
        self.ventana_principal.deiconify()