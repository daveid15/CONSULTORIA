import tkinter as tk

ventana = tk.Tk()
ventana.title("Ventana 1") 
ventana.geometry("400x300") 

boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton_cerrar.pack(pady=10)

ventana.mainloop()