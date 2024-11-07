import calendar
import json
import random
from turtle import home
import pandas as pd
from datetime import datetime, time, timedelta
from django.utils import timezone
from datetime import datetime
import pytz
import xlwt
from django.http import HttpResponse
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, GroupManager, User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from dateutil import relativedelta
from registration.models import Profile
from core.views import *
#validaciones .py!!!!! <---------------------------------
from extensiones import validacion
#from django.shortcuts import render, get_object_or_404, redirect
from .models import Perfil_Parametro, Prueba #, Medicion
from .forms import PerfilParametroForm ##, PruebaForm, MedicionForm
import pyvisa
import numpy as np
from django.http import JsonResponse
import time


num_elemento = num_pag()#desde core se importa el numero de elementos por página

def ejecutar_medicion(start_current, step_size, delay, simular=False):
    resultados = []

    if simular:  # Modo de simulación
        corrientes = np.linspace(start_current, -start_current, num=step_size)
        for corriente in corrientes:
            V = corriente*2
            resultados.append((round(corriente,1), round(V,1)))
            time.sleep(delay)  # Simula el tiempo de espera
    else:
        try:
            rm = pyvisa.ResourceManager()
            with rm.open_resource('GPIB0::9::INSTR') as multimetro:
                # Configurar el multímetro
                multimetro.write("*RST")
                multimetro.write(":SOUR:FUNC CURR")
                multimetro.write("CONF:VOLT:DC")
                multimetro.write("OUTPUT ON")

                # Calcular corrientes
                corrientes = np.linspace(start_current, -start_current, num=step_size)

                for corriente in corrientes:
                    try:
                        multimetro.write(f":SOUR:CURR {corriente}")
                        time.sleep(delay)
                        medida_voltaje = multimetro.query(":MEAS:VOLT:DC?")
                        valores = medida_voltaje.strip().split(',')
                        V = float(valores[0])
                        resultados.append((corriente, V))
                    except Exception:
                        resultados.append((corriente, None))  # Guarda None si hay un error

                multimetro.write("OUTPUT OFF")

        except Exception as e:
            return {'error': f"No se pudo conectar al multímetro: {str(e)}"}

    return {'resultados': resultados}



def medir_iv_view(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    array_current = [0]
    array_voltaje = [0]
    if request.method == 'POST':
        # Obtener parámetros del formulario
        start_current = float(request.POST.get('start_current', 0))
        step_size = int(request.POST.get('step_size', 1))
        delay = float(request.POST.get('delay', 0))

        # Ejecutar medición
        resultado = ejecutar_medicion(start_current, step_size, delay, simular=True)  # Cambia a False si no es simulación
        
        current, voltaje  = zip(*resultado['resultados'])
        array_current = list(current)
        array_voltaje = list(voltaje)
        print(resultado)
    template_name = 'caracterizacion/medir_iv.html'
    return render(request,template_name,{'profiles':profiles,
                                        'currents': array_current, 
                                        'volts': array_voltaje})
@login_required
def caracterizacion_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    check_profile_admin(request, profiles)
    template_name = 'caracterizacion/caracterizacion_main.html'
    return render(request,template_name,{'profiles':profiles})
#Flujo usuarios

@login_required
def grafico (request):
    profiles = Profile.objects.get(user_id = request.user.id)
    check_profile_admin(request, profiles)
    array_voltaje = [0, 1.2, 2.4, 3.5, 4.9, 6.1, 7.3, 8.6, 9.8, 11]
    array_current = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    template_name = 'caracterizacion/grafico.html'
    return render(request,template_name,{'profiles':profiles,
                                        'currents': array_current, 
                                        'volts': array_voltaje})



# Listar perfiles de parámetros
@login_required
def listar_perfiles(request):
    #perfiles = Perfil_Parametro.objects.all()
    perfiles = Perfil_Parametro.objects.filter(perfil_parametro_state='t')  # Mostrar solo perfiles activos
    return render(request, 'caracterizacion/listar_perfiles.html', {'perfiles': perfiles})

# Crear un perfil de parámetros 
@login_required
def crear_perfil(request):
    if request.method == 'POST':
        nombre_perfil = request.POST.get('perfil_parametro_name')
        if Perfil_Parametro.objects.filter(perfil_parametro_name=nombre_perfil).exists():
            error_message = "El nombre del perfil ya existe. Por favor, elija otro."
            return render(request, 'caracterizacion/crear_perfil.html', {'error_message': error_message})
        else:

            form = PerfilParametroForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'¡Perfil creado correctamente!')
                return redirect('listar_perfiles')
    else:
        form = PerfilParametroForm()
    return render(request, 'caracterizacion/crear_editar_perfil.html', {'form': form})

# Editar un perfil de parámetros
@login_required
def editar_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        form = PerfilParametroForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request,'¡Perfil '+perfil.perfil_parametro_name+' actualizado correctamente!')
            return redirect('listar_perfiles')
    else:
        form = PerfilParametroForm(instance=perfil)
    return render(request, 'caracterizacion/crear_editar_perfil.html', {'form': form, 'perfil': perfil})


# Eliminar un perfil de parámetros
@login_required
def eliminar_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        messages.success(request,'¡Perfil eliminado correctamente!')
        return redirect('listar_perfiles')
    return render(request, 'caracterizacion/eliminar_perfil.html', {'perfil': perfil})

# Ver un perfil de parámetros
@login_required
def detalle_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    return render(request, 'caracterizacion/detalle_perfil.html', {'perfil': perfil})

@login_required
def bloquear_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.perfil_parametro_state = 'f'
    perfil.save()
    try:

        messages.success(request, 'Perfil '+perfil.perfil_parametro_name + 'bloqueado con éxito')
        return redirect('listar_perfiles')
    except:
        messages.error(request, 'El perfil '+perfil.perfil_parametro_name + ' no se ha podido bloquear')
        return redirect('listar_perfiles')

@login_required
def listar_perfiles_bloqueados(request):
    perfiles_bloqueados = Perfil_Parametro.objects.filter(perfil_parametro_state='f')  # Mostrar solo perfiles bloqueados
    return render(request, 'caracterizacion/perfiles_bloqueados.html', {'perfiles_bloqueados': perfiles_bloqueados})

@login_required
def desbloquear_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.perfil_parametro_state = 't'
    perfil.save()
    try:
        messages.success(request, 'Perfil '+perfil.perfil_parametro_name + 'desbloqueado con éxito')
        return redirect('listar_perfiles_bloqueados')
    except:
        messages.error(request, 'El perfil '+perfil.perfil_parametro_name + ' no se ha podido desbloquear')
        return redirect('listar_perfiles_bloqueados')

    

@login_required
def eliminar_perfil_bloqueado(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.delete()
    return redirect('listar_perfiles_bloqueados')

# Apartado prueba

@login_required
def listar_pruebas(request):
    pruebas = Prueba.objects.all()
    return render(request, 'caracterizacion/listar_pruebas.html', {'pruebas': pruebas})

@login_required
def eliminar_prueba(request, pk):
    prueba = get_object_or_404(Prueba, pk=pk)
    if request.method == 'POST':
        prueba.delete()
        return redirect('listar_pruebas')
    return render(request, 'caracterizacion/eliminar_prueba.html', {'prueba': prueba})