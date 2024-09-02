import tkinter as tk

class Ventana4:
    def __init__(self, menu, ventana_principal):
        self.menu = menu
        self.ventana_principal = ventana_principal
        self.menu.title("Pruebas")
        self.menu.geometry("800x600")
        self.menu.configure(bg="royalblue4")

        #Titulos
        titulo1 = tk.Label(self.menu, text="Historial de Pruebas")
        titulo1.place(x=100, y=50)
        #Botones
        btn_volver = tk.Button(self.menu, text="volver a menu", command=self.volver)
        btn_volver.place(x=100, y=100)

    def volver(self):
        self.menu.withdraw()  
        self.ventana_principal.deiconify()