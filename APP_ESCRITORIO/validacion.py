# Archivo validacion.py
from tkinter import messagebox
import pyvisa
def validar_float(valor):
    try:
        # Intentar convertir el valor a float
        return float(valor)
    except ValueError:
        return None


def validar_int(valor):
    try:
        # Intentar convertir el valor a int
        return int(valor)
    except ValueError:
        return None
    

def listar_recursos():
    rm = pyvisa.ResourceManager()
    recursos = rm.list_resources()
    if recursos:
        print("Recursos disponibles:")
        for recurso in recursos:
            print(recurso)
    else:
        print("No se encontraron recursos.")




def verificar_dispositivo(resource_address, parent_window):
    rm = pyvisa.ResourceManager()
    try:
        # Intenta abrir el recurso
        """instrumento = rm.open_resource(f"GPIB0::{resource_address}::INSTR")
        messagebox.showinfo("Conexión exitosa", 
                            f"El dispositivo GPIB0::{resource_address}::INSTR está conectado.",
                            parent=parent_window)
        
        # Puedes enviar un comando simple para verificar la respuesta
        respuesta = instrumento.query("*IDN?")
        messagebox.showinfo("Respuesta del dispositivo", 
                            f"Respuesta del dispositivo: {respuesta}",
                            parent=parent_window)"""
        return True
    except pyvisa.VisaIOError as e:
        messagebox.showerror("Error de conexión", 
                            f"No se pudo conectar con el dispositivo GPIB0::{resource_address}::INSTR",
                            parent=parent_window)
        return False
    finally:
        # Cierra la conexión con el recurso si se abrió correctamente
        if 'instrumento' in locals():
            instrumento.close()



def verificar_inputs(start_current_str, step_size_str, delay_str, parent_window):
    errores = []

    # Validar cada input
    start_current = validar_float(start_current_str)
    if start_current is None or start_current <= 0:
        errores.append("El valor de 'Intervalo Simétrico ' debe ser un número mayor a cero.")
    elif validar_intervalo_simetrico(start_current):
        errores.append("El valor del intervalo simétrico debe estar entre 1 pA y 1.05 A")
    step_size = validar_int(step_size_str)
    if step_size is None or step_size <= 0:

        errores.append("El valor de 'Intervalos de Corriente' debe ser un número entero mayor a cero.")

    delay = validar_float(delay_str)
    if delay is None or delay <= 0:
        errores.append("El valor de 'Tiempo entre Mediciones' debe ser un número flotante mayor a cero.")


    if errores:
        # Mostrar errores
        mensaje_error = "\n".join(errores)
        messagebox.showerror("Errores de Validación", mensaje_error, parent=parent_window)
        return False
    else:
        return True
    
    
def validar_intervalo_simetrico(start_current):
    min_current = 1e-12
    max_current = 1.05
    if ( start_current >=min_current and start_current <= max_current):
        return False
    else:
        return True