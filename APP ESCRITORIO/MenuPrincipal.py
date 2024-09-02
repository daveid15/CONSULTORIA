import tkinter as tk
from ventana1 import Ventana1
from ventana2 import Ventana2
from ventana3 import Ventana3
from ventana4 import Ventana4

class MenuPrincipal:
    def __init__(self,menu):
        self.menu = menu
        self.menu.title("Menú Principal")
        self.menu.geometry("800x600")
        self.menu.configure(bg="royalblue4")

        #Titulos
        titulo1 = tk.Label(self.menu, text="MENÚ PRINCIPAL")
        titulo1.place(x=300, y=50)
        # Botones
        btn_ventana1 = tk.Button(self.menu, text="Caracterización Eléctrica", command=self.abrir_ventana1)
        btn_ventana1.place(x=100, y=100)
        btn_ventana2 = tk.Button(self.menu, text="Caracterización Magneto-Electrica", command=self.abrir_ventana2)
        btn_ventana2.place(x=100, y=150)
        btn_ventana3 = tk.Button(self.menu, text="Caracterización Magneto-Electrica INVERTIDA", command=self.abrir_ventana3)
        btn_ventana3.place(x=100, y=200)
        btn_ventana4 = tk.Button(self.menu, text="Pruebas", command=self.abrir_ventana4)
        btn_ventana4.place(x=100, y=250)

        self.menu.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def abrir_ventana1(self):
        self.menu.withdraw()
        nueva_ventana = tk.Toplevel(self.menu)
        Ventana1(nueva_ventana, self.menu)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def abrir_ventana2(self):
        self.menu.withdraw()
        nueva_ventana = tk.Toplevel(self.menu)
        Ventana2(nueva_ventana, self.menu)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def abrir_ventana3(self):
        self.menu.withdraw()
        nueva_ventana = tk.Toplevel(self.menu)
        Ventana3(nueva_ventana, self.menu)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def abrir_ventana4(self):
        self.menu.withdraw()
        nueva_ventana = tk.Toplevel(self.menu)
        Ventana4(nueva_ventana, self.menu)
        nueva_ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        self.menu.quit() 
        self.menu.destroy()

if __name__ == "__main__":
    menu = tk.Tk()
    app = MenuPrincipal(menu)
    menu.mainloop()
