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
from .models import Perfil_Parametro ##Prueba, Medicion
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
            V = random.uniform(-5, 5)  # Simula un voltaje entre -5 y 5 V
            resultados.append((corriente, V))
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
    if request.method == 'POST':
        # Obtener parámetros del formulario
        start_current = float(request.POST.get('start_current', 0))
        step_size = int(request.POST.get('step_size', 1))
        delay = float(request.POST.get('delay', 0))

        # Ejecutar medición
        resultado = ejecutar_medicion(start_current, step_size, delay, simular=True)  # Cambia a False si no es simulación

        if 'error' in resultado:  # Verifica si hubo un error
            return JsonResponse({'error': resultado['error']})

        return JsonResponse({'resultados': resultado['resultados']})

    return render(request, 'caracterizacion/medir_iv.html')
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
def listar_perfiles(request):
    #perfiles = Perfil_Parametro.objects.all()
    perfiles = Perfil_Parametro.objects.filter(perfil_parametro_state='t')  # Mostrar solo perfiles activos
    return render(request, 'caracterizacion/listar_perfiles.html', {'perfiles': perfiles})

# Crear un perfil de parámetros
def crear_perfil(request):
    if request.method == 'POST':
        form = PerfilParametroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_perfiles')
    else:
        form = PerfilParametroForm()
    return render(request, 'caracterizacion/crear_editar_perfil.html', {'form': form})

# Editar un perfil de parámetros
def editar_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        form = PerfilParametroForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('listar_perfiles')
    else:
        form = PerfilParametroForm(instance=perfil)
    return render(request, 'caracterizacion/crear_editar_perfil.html', {'form': form, 'perfil': perfil})

# Eliminar un perfil de parámetros
def eliminar_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        return redirect('listar_perfiles')
    return render(request, 'caracterizacion/eliminar_perfil.html', {'perfil': perfil})

# Ver un perfil de parámetros
def detalle_perfil(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    return render(request, 'caracterizacion/detalle_perfil.html', {'perfil': perfil})

<<<<<<< HEAD
def bloquear_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    #perfil.bloqueado = True
    perfil.perfil_parametro_state = 'f'
    perfil.save()
    return redirect('listar_perfiles')  # Redirige a la lista de perfiles

def listar_perfiles_bloqueados(request):
    #perfiles_bloqueados = Perfil_Parametro.objects.filter(bloqueado=True)
    perfiles_bloqueados = Perfil_Parametro.objects.filter(perfil_parametro_state='f')  # Mostrar solo perfiles bloqueados
    return render(request, 'caracterizacion/perfiles_bloqueados.html', {'perfiles_bloqueados': perfiles_bloqueados})


def eliminar_perfil_bloqueado(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.delete()
    return redirect('listar_perfiles_bloqueados')
=======
>>>>>>> 94863ca128b7d6a32e2a90c9ec292f7385266384
