import tkinter as tk
from tkinter import messagebox
import nidaqmx
from nidaqmx.constants import LineGrouping

# Definimos las configuraciones disponibles
configuraciones = [
    ((True, False, False, True), "Aplicar Configuración 1", "Configuración 1: A -> D (corriente) y B -> C (medición)"),
    ((True, False, True, False), "Aplicar Configuración 2", "Configuración 2: A -> C (corriente) y B -> D (medición)"),
    ((False, True, False, True), "Aplicar Configuración 3", "Configuración 3: B -> D (corriente) y A -> C (medición)"),
    ((False, True, True, False), "Aplicar Configuración 4", "Configuración 4: B -> C (corriente) y A -> D (medición)")
]

# Estado inicial de los pines
estados_reles = [False] * 4  # Inicialmente, todos los relés están apagados

# Función para cambiar el estado de los pines
def cambiar_estado_pines(estados):
    pines = ["Dev1/port0/line0", "Dev1/port0/line1", "Dev1/port0/line2", "Dev1/port0/line3"]

    try:
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(", ".join(pines), line_grouping=LineGrouping.CHAN_PER_LINE)
            task.write(estados, auto_start=True)  # Aseguramos que 'estados' tenga 4 elementos
            return True
    except nidaqmx.errors.DaqError as e:
        messagebox.showerror("Error", f"No se pudo cambiar la configuración: {e}")
        return False

# Función para aplicar una configuración y actualizar la retroalimentación
def aplicar_configuracion(nuevos_estados, descripcion):
    global estados_reles  # Hacemos referencia a la variable global

    # Verificamos si los nuevos estados son diferentes de los actuales
    if list(nuevos_estados) != estados_reles:
        exito = cambiar_estado_pines(list(nuevos_estados))  # Convertimos a lista para asegurarnos
        if exito:
            estados_reles = list(nuevos_estados)  # Actualizamos el estado de los relés
            retroalimentacion_label.config(text=f"Configuración aplicada: {descripcion}", fg="green")
    else:
        messagebox.showinfo("Información", "La configuración ya está aplicada.")

# Configuración de la ventana principal con Tkinter
ventana = tk.Tk()
ventana.title("Control de Configuraciones de Relés")
ventana.geometry("400x300")

frame = tk.Frame(ventana)
frame.pack(pady=20)

# Crear botones para cada configuración
for estados, texto_boton, descripcion in configuraciones:
    boton = tk.Button(frame, text=texto_boton, command=lambda e=estados, d=descripcion: aplicar_configuracion(e, d))
    boton.pack(pady=5)

# Label para retroalimentación
retroalimentacion_label = tk.Label(ventana, text="Ninguna configuración aplicada", fg="red")
retroalimentacion_label.pack(pady=20)

# Iniciar el bucle principal de Tkinter
ventana.mainloop()
