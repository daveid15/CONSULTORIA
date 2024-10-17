# Archivo validacion.py
from tkinter import messagebox
import pyvisa
import json
import os
import nidaqmx
from nidaqmx.errors import DaqError
#****VALIDACIONES DE INPUTS*****

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
    


#****VALIDACIONES DE COMUNICACIÓN*****
def listar_recursos():
    rm = pyvisa.ResourceManager()
    recursos = rm.list_resources()
    if recursos:
        print("Recursos disponibles:")
        for recurso in recursos:
            print(recurso)
    else:
        print("No se encontraron recursos.")


def validar_conexion_gauss(errores, parent_window = None):
    #Valida si el Gauss meter está conectado correctamente.
    try:
        with nidaqmx.Task() as task:
            # Intenta agregar el canal de voltaje del Gauss meter
            task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
            # Si no se produce ningún error, está conectado
            if parent_window:
                return True
            return errores
    except DaqError as e:
        # Mostrar advertencia si no se puede conectar al dispositivo
        if parent_window:
            messagebox.showerror("Error de conexión", 
                        f"No se pudo conectar con el GaussMeter en el canal Dev2/ai0",
                        parent=parent_window)
            return False
        errores.append(f"No se pudo conectar con el GaussMeter en el canal Dev2/ai0")
        return errores



def verificar_dispositivo(addresses, parent_window):
    errores = []
    rm = pyvisa.ResourceManager()
    for address in addresses:
        try:
            # Intenta abrir el recurso
            instrumento = rm.open_resource(f"GPIB0::{address}::INSTR")
            """messagebox.showinfo("Conexión exitosa", 
                                f"El dispositivo GPIB0::{resource_address}::INSTR está conectado.",
                                parent=parent_window)
            
            # Puedes enviar un comando simple para verificar la respuesta
            respuesta = instrumento.query("*IDN?")
            messagebox.showinfo("Respuesta del dispositivo", 
                                f"Respuesta del dispositivo: {respuesta}",
                                parent=parent_window)"""
            return True
        except pyvisa.VisaIOError as e:
            errores.append(f"Error de conexión, No se pudo conectar con el dispositivo GPIB0::{address}::INSTR")
        
    # Cierra la conexión con el recurso si se abrió correctamente
    if 'instrumento' in locals():
        instrumento.close()
    if errores:
        errores = validar_conexion_gauss(errores)
        # Mostrar errores
        mensaje_error = "\n".join(errores)
        messagebox.showerror("Errores de Validación", mensaje_error, parent=parent_window)
        return False



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
    elif validar_delay(delay):
        errores.append("El valor de 'Tiempo entre Mediciones' debe entre 1ms y 999.999s .")

    if errores:
        # Mostrar errores
        mensaje_error = "\n".join(errores)
        messagebox.showerror("Errores de Validación", mensaje_error, parent=parent_window)
        return False
    else:
        return True
    
    
    
def verificar_inputs_gauss(start_saturation, constant_current_str, step_size_str, delay_str, parent_window):
    errores = []

    # Validar cada input
    constant_current = validar_float(constant_current_str)
    if constant_current is None or constant_current <= 0:
        errores.append("El valor de 'Corriente Fija' debe ser un número mayor a cero.")
    elif validar_intervalo_simetrico(constant_current):
        errores.append("El valor de 'Corriente Fija' debe estar entre 1 pA y 1.05 A")
    step_size = validar_int(step_size_str)
    start_saturation=validar_int(start_saturation)
    if start_saturation is None or start_saturation <= 0:
        errores.append("El valor de 'Saturación de Campo' debe ser un número entero mayor a cero.")
    elif validar_saturacion_campo(start_saturation):
        errores.append("El valor de 'Saturación de Campo' debe estar entre -5000G y 5000G.")
    if step_size is None or step_size <= 0:
        errores.append("El valor de 'Intervalos de Corriente' debe ser un número entero mayor a cero.")
    
    delay = validar_float(delay_str)
    if delay is None or delay <= 0:
        errores.append("El valor de 'Tiempo entre Mediciones' debe ser un número flotante mayor a cero.")
    elif validar_delay(delay):
        errores.append("El valor de 'Tiempo entre Mediciones' debe entre 1ms y 999.999s .")

    if errores:
        # Mostrar errores
        mensaje_error = "\n".join(errores)
        messagebox.showerror("Errores de Validación", mensaje_error, parent=parent_window)
        return False
    else:
        return True
        
    
def validar_saturacion_campo(start_field):
    min_field = -5000
    max_field = 5000
    if ( start_field >=min_field and start_field <= max_field):
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
    
def validar_delay(delay):
    min_delay = 0.001
    max_delay = 999.999
    if ( delay >=min_delay and delay <= max_delay):
        return False
    else:
        return True
    
def comparar_perfiles(perfil1, perfil2):
    #compara dos perfiles
    return (
        perfil1['intervalo_simetrico'] == perfil2['intervalo_simetrico'] and
        perfil1['intervalos_corriente'] ==perfil2['intervalos_corriente'] and
        perfil1['tiempo_entre_mediciones'] == perfil2['tiempo_entre_mediciones']
    )

def validar_perfil(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones):
    json_path = os.path.join('perfiles_parametros.json')
    try:
        with open(json_path, 'r') as file:
            datos_perfiles = json.load(file)

        perfil_nuevo = {
            'intervalo_simetrico': str(intervalo_simetrico),
            'intervalos_corriente': str(intervalos_corriente),
            'tiempo_entre_mediciones': str(tiempo_entre_mediciones)
        }

        for nombres in datos_perfiles:
            #compara los nombres existentes con el ingresado
            if nombres != nombre:
                for perfil in datos_perfiles.values():
                    #compara el perfil ingresado don el que esta iterando
                    if (comparar_perfiles(perfil, perfil_nuevo)):
                        print(comparar_perfiles(perfil, perfil_nuevo))
                        messagebox.showwarning('Advertencia','Ya existe un perfil con esos datos')
                        return False
                    return False
            else:
                messagebox.showwarning('Advertencia', 'Ya existe un perfil con ese nombre')
                return False
        guardar_txt(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones)
        return True
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror('Error', f'Error al cargar los perfiles: {str(e)}')
        return False
    
def guardar_txt(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones):
    f = open("perfiles_parametros.txt", "a")
    f.write(f"{nombre} | {intervalo_simetrico} | {intervalos_corriente} | {tiempo_entre_mediciones} | \n")
    f.close()

validar_perfil('Prueba 3', 20, 20, 20)