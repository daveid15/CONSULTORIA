# Archivo validacion.py
from tkinter import messagebox
import pyvisa
import json
import os
import nidaqmx
from nidaqmx.errors import DaqError
import numpy as np
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


def validar_conexion_gauss(errores, parent_window):
    """
    Valida si el Gaussímetro está conectado correctamente a través de la tarjeta DAQ.
    Se calcula la diferencia entre el valor promedio de las mediciones y los valores de referencia de apagado y encendido.

    :param errores: Lista para agregar mensajes de error.
    :param parent_window: Interfaz gráfica o ventana principal (no utilizada en este fragmento, pero podría ser útil para actualizaciones en GUI).
    :return: Lista de errores (vacía si no hay errores).
    """
    try:
        # Configuración de la tarea de adquisición de datos
        with nidaqmx.Task() as task:
            num_samples = 10  # Número de muestras a tomar
            sample_rate = 1000  # Frecuencia de muestreo en Hz
            task.ai_channels.add_ai_voltage_chan("Dev2/ai0")  # Canal de entrada (cambiar según tu configuración)

            # Configuración del temporizador de adquisición de datos
            task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=num_samples)

            # Leer las muestras de datos
            data = task.read(num_samples)
            # Convertir los datos a un array de numpy
            data_array_0 = np.array(data)


            # Promediar los datos para obtener una medida representativa
            promedio_data_0 = np.mean(data_array_0)


            # Definir los valores de referencia de apagado y encendido
            valor_apagado = -0.004829086130484939
            valor_encendido = -0.008696450851857662

            # Comparar el valor promedio con los valores de referencia
            diferencia_apagado = abs(promedio_data_0 - valor_apagado)
            diferencia_encendido = abs(promedio_data_0 - valor_encendido)



            # Umbral de diferencia, que se ajusta según el comportamiento esperado de los datos
            umbral_diferencia = 0.0038673647213727236

            # Validar si la diferencia es suficientemente grande
            if diferencia_apagado > umbral_diferencia and diferencia_encendido > umbral_diferencia:
                errores.append(f"No se pudo conectar correctamente al GaussMeter en el canal Dev2/ai0. La diferencia es demasiado grande.")
                return errores

            # Si la diferencia es válida, la conexión está funcionando correctamente

            return errores

    except DaqError as e:
        # Manejo de errores específicos de DAQmx
        errores.append(f"Error de DAQmx: {str(e)}. No se pudo conectar al GaussMeter en el canal Dev2/ai0.")
        return errores

    except Exception as e:
        # Manejo de cualquier otro tipo de error
        errores.append(f"Error inesperado: {str(e)}")
        return errores



def verificar_dispositivo(addresses, parent_window, gauss):
    errores = []
    rm = pyvisa.ResourceManager()
    for address in addresses:
        try:
            # Intenta abrir el recurso
            instrumento = rm.open_resource(f"GPIB0::{address}::INSTR")
            respuesta = instrumento.query("*IDN?")
            """messagebox.showinfo("Conexión exitosa", 
                                f"El dispositivo GPIB0::{resource_address}::INSTR está conectado.",
                                parent=parent_window)
            
            # Puedes enviar un comando simple para verificar la respuesta
            
            messagebox.showinfo("Respuesta del dispositivo", 
                                f"Respuesta del dispositivo: {respuesta}",
                                parent=parent_window)"""
            return True
        except pyvisa.VisaIOError as e:
            errores.append(f"Error de conexión, No se pudo conectar con el dispositivo GPIB0::{address}::INSTR")
        
    # Cierra la conexión con el recurso si se abrió correctamente
    if 'instrumento' in locals():
        instrumento.close()
    if gauss:
        errores = validar_conexion_gauss(errores, parent_window)

    if errores:
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
        
    delay = validar_float(delay_str)
    if delay is None or delay <= 0:
        errores.append("El valor de 'Tiempo entre Mediciones' debe ser un número flotante mayor a cero.")
    elif validar_delay(delay):
        errores.append("El valor de 'Tiempo entre Mediciones' debe entre 1ms y 999.999s .")
    if step_size is None or step_size <= 0:
        errores.append("El valor de 'Intervalos de Campos' debe ser un número entero mayor a cero.")
    


    if errores:
        # Mostrar errores
        mensaje_error = "\n".join(errores)
        messagebox.showerror("Errores de Validación", mensaje_error, parent=parent_window)
        return False
    else:
        return True
        

def verificar_inputs_ecuacion(start_voltaje_str, step_size_str, delay_str, parent_window):
    errores = []
    # Validar cada input
    start_voltaje = validar_float(start_voltaje_str)
    if start_voltaje is None or start_voltaje <= 0:
        errores.append("El valor de 'intervalo simétrico ' debe ser un número mayor a cero.")
    elif validar_intervalo_simetrico_voltaje(start_voltaje):
        errores.append("El valor del intervalo simétrico debe estar entre 20 V y 1 V")
    step_size = validar_int(step_size_str)
    if step_size is None or step_size <= 0:
        errores.append("El valor de 'Intervalos de Voltajes' debe ser un número entero mayor a cero.")
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
    
def validar_intervalo_simetrico_voltaje(start_voltaje):
    min_voltaje = 1
    max_voltaje = 20
    if ( start_voltaje >=min_voltaje and start_voltaje <= max_voltaje):
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
    #compara dos perfiles ingresados en la ventana 1
    return (
        perfil1['intervalo_simetrico'] == perfil2['intervalo_simetrico'] and
        perfil1['intervalos_corriente'] == perfil2['intervalos_corriente'] and
        perfil1['tiempo_entre_mediciones'] == perfil2['tiempo_entre_mediciones']
    )

def validar_perfil_v1(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones):
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
                        messagebox.showwarning('Advertencia','Ya existe un perfil con esos datos')
                        return False
                    
            else:
                messagebox.showwarning('Advertencia', 'Ya existe un perfil con ese nombre')
                
                return False
        #guardar_txt(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones)
        return True
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror('Error', f'Error al cargar los perfiles: {str(e)}')
        return False
    
def guardar_txt(nombre, intervalo_simetrico, intervalos_corriente, tiempo_entre_mediciones):
    f = open("v1_perfiles_parametros.txt", "a")
    f.write(f"{nombre} | {intervalo_simetrico} | {intervalos_corriente} | {tiempo_entre_mediciones} | \n")
    f.close()


def comparar_perfiles_v2(perfil1, perfil2):
    return (
        perfil1['corriente_fija'] == perfil2['corriente_fija'] and
        perfil1['saturacion_campo'] == perfil2['saturacion_campo'] and
        perfil1['tiempo_entre_mediciones_v2'] == perfil2['tiempo_entre_mediciones_v2'] and
        perfil1['pasos'] == perfil2['pasos']
    )

def validar_perfil_v2(nombre, corriente_fija, saturacion_campo, tiempo_entre_mediciones_v2, pasos):
    json_path = os.path.join('APP_ESCRITORIO', 'perfiles_parametros2.json')
    
    try:
        with open(json_path, 'r') as file:
            datos_perfiles = json.load(file)
        
        perfil_nuevo = {
            'corriente_fija': str(corriente_fija),
            'saturacion_campo': str(saturacion_campo),
            'tiempo_entre_mediciones_v2': str(tiempo_entre_mediciones_v2),
            'pasos': str(pasos)
        }
        
        for nombre_existente, perfil_existente in datos_perfiles.items():
            if comparar_perfiles_v2(perfil_existente, perfil_nuevo):
                messagebox.showwarning('Advertencia', 'Ya existe un perfil con esos datos')
                return False
            elif nombre_existente == nombre:
                messagebox.showwarning('Advertencia', 'Ya existe un perfil con ese nombre')
                return False

        # Guardar nuevo perfil en el archivo JSON
        datos_perfiles[nombre] = perfil_nuevo
        with open(json_path, 'w') as file:
            json.dump(datos_perfiles, file, indent=4)

        # Guardar también en el archivo TXT
        guardar_txt_v2(nombre, corriente_fija, saturacion_campo, tiempo_entre_mediciones_v2, pasos)
        
        return True

    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está corrupto, crearlo con el perfil actual
        with open(json_path, 'w') as file:
            json.dump({nombre: perfil_nuevo}, file, indent=4)
        
        guardar_txt_v2(nombre, corriente_fija, saturacion_campo, tiempo_entre_mediciones_v2, pasos)
        return True
    
def guardar_txt_v2(nombre, corriente_fija, saturacion_campo, tiempo_entre_mediciones_v2, pasos):
    ruta_archivo = os.path.join('APP_ESCRITORIO', 'v2_perfiles_parametros2.txt')
    
    with open(ruta_archivo, 'a') as f:
        f.write(f"{nombre} | {corriente_fija} | {saturacion_campo} | {tiempo_entre_mediciones_v2} | {pasos} |\n")


def comparar_perfiles_v3(perfil1, perfil2):
    # Asegurarse de que ambos perfiles tienen las claves necesarias
    keys = ['corriente_fija_v3', 'saturacion_campo_v3', 'tiempo_entre_mediciones_v3']
    if all(key in perfil1 for key in keys) and all(key in perfil2 for key in keys):
        return (
            perfil1['corriente_fija_v3'] == perfil2['corriente_fija_v3'] and
            perfil1['saturacion_campo_v3'] == perfil2['saturacion_campo_v3'] and
            perfil1['tiempo_entre_mediciones_v3'] == perfil2['tiempo_entre_mediciones_v3']
        )
    else:
        raise KeyError("Uno de los perfiles no tiene todas las claves necesarias.")

def validar_perfil_v3(nombre, corriente_fija_v3, saturacion_campo_v3, tiempo_entre_mediciones_v3, intervalos_campos_v3):
    json_path = os.path.join('perfiles_ventana3.json')
    try:
        with open(json_path, 'r') as file:
            datos_perfiles = json.load(file)

        perfil_nuevo = {
            'corriente_fija_v3': str(corriente_fija_v3),
            'saturacion_campo_v3': str(saturacion_campo_v3),
            'tiempo_entre_mediciones_v3': str(tiempo_entre_mediciones_v3),
            'intervalos_campos_v3': str(intervalos_campos_v3)
        }

        for nombres, perfil_existente in datos_perfiles.items():
            if nombres != nombre:
                if comparar_perfiles_v3(perfil_existente, perfil_nuevo):
                    messagebox.showwarning('Advertencia', 'Ya existe un perfil con esos datos')
                    return False
            else:
                messagebox.showwarning('Advertencia', 'Ya existe un perfil con ese nombre')
                return False

        # Guarda el nuevo perfil
        datos_perfiles[nombre] = perfil_nuevo
        with open(json_path, 'w') as file:
            json.dump(datos_perfiles, file, indent=4)

        guardar_txt_v3(nombre, corriente_fija_v3, saturacion_campo_v3, tiempo_entre_mediciones_v3, intervalos_campos_v3)
        return True

    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror('Error', f'Error al cargar los perfiles: {str(e)}')
        return False
    
def guardar_txt_v3(nombre, corriente_fija_v3, saturacion_campo_v3, tiempo_entre_mediciones_v3, intervalos_campos_v3):
    ruta_txt = "v3_perfiles_parametros.txt"
    with open(ruta_txt, "a") as f:
        f.write(f"{nombre} | {corriente_fija_v3} | {saturacion_campo_v3} | {tiempo_entre_mediciones_v3} | {intervalos_campos_v3} |\n")




def centrar_ventana(ventana, ancho_ventana, alto_ventana):
    """
    Centra una ventana en la pantalla.
    
    Args:
    - ventana: la ventana de Tkinter que se quiere centrar.
    - ancho_ventana: el ancho deseado para la ventana.
    - alto_ventana: la altura deseada para la ventana.
    """
    # Obtener el tamaño de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular la posición centrada
    x_centrado = (ancho_pantalla - ancho_ventana) // 2
    y_centrado = (alto_pantalla - alto_ventana) // 2
    
    # Configurar las dimensiones y posición de la ventana
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_centrado}+{y_centrado}")