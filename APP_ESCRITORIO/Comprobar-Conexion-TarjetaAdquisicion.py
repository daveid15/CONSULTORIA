import tkinter as tk
from tkinter import messagebox
import nidaqmx
from nidaqmx.constants import LineGrouping

# Definimos las configuraciones disponibles
configuraciones = [
    ((True, False, False, True), "Aplicar Configuración 1", "A -> D (corriente) y B -> C (medición)"),
    ((True, False, True, False), "Aplicar Configuración 2", "A -> C (corriente) y B -> D (medición)"),
    ((False, True, False, True), "Aplicar Configuración 3", "B -> D (corriente) y A -> C (medición)"),
    ((False, True, True, False), "Aplicar Configuración 4", "B -> C (corriente) y A -> D (medición)")
]

# Estado inicial de los pines
estados_reles = [False] * 4  # Inicialmente, todos los relés están apagados (False)

# Función para cambiar el estado de los pines
def cambiar_estado_pines(estados):
    pines = ["Dev2/port0/line0", "Dev2/port0/line1", "Dev2/port0/line2", "Dev2/port0/line3"]

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
            print(f"Estado de los relés actualizado: {estados_reles}")  # Agrega este print para ver los estados
    else:
        messagebox.showinfo("Información", "La configuración ya está aplicada.")

# Función para reiniciar los relés a False
def reiniciar_reles():
    global estados_reles
    estados_reles = [False] * 4  # Todos los relés en False
    exito = cambiar_estado_pines(estados_reles)
    if exito:
        retroalimentacion_label.config(text="Todos los relés se han APAGADO.", fg="blue")
        print(f"Estado de los relés reiniciado: {estados_reles}")

# Configuración de la ventana principal con Tkinter
ventana = tk.Tk()
ventana.title("Control de Configuraciones de Relés")
ventana.geometry("400x350")

frame = tk.Frame(ventana)
frame.pack(pady=20)

# Crear botones para cada configuración
for estados, texto_boton, descripcion in configuraciones:
    boton = tk.Button(frame, text=texto_boton, command=lambda e=estados, d=descripcion: aplicar_configuracion(e, d))
    boton.pack(pady=5)

# Botón para reiniciar todos los relés a OFF (False)
boton_reiniciar = tk.Button(ventana, text="APAGAR Relés", command=reiniciar_reles)
boton_reiniciar.pack(pady=10)

# Label para retroalimentación
retroalimentacion_label = tk.Label(ventana, text="Ninguna configuración aplicada", fg="red")
retroalimentacion_label.pack(pady=20)

# Inicializamos todos los relés en OFF (False) al iniciar la aplicación
reiniciar_reles()  # Llamamos a la función para inicializar los relés en False al inicio

# Iniciar el bucle principal de Tkinter
ventana.mainloop()
