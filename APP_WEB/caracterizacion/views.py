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
from .models import Perfil_Parametro,Prueba, Medicion
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
        
        # Comprobar si el nombre ya existe
        if Perfil_Parametro.objects.filter(perfil_parametro_name=nombre_perfil).exists():
            error_message = "El nombre del perfil ya existe. Por favor, elija otro."
            return render(request, 'caracterizacion/crear_perfil.html', {'error_message': error_message})
        
        # Continuar con el proceso de guardado si no existe
        else:
            # Crear el perfil con los demás campos
            form = PerfilParametroForm(request.POST)
            if form.is_valid():
                form.save()
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
    return redirect('listar_perfiles')  # Redirige a la lista de perfiles

@login_required
def listar_perfiles_bloqueados(request):
    perfiles_bloqueados = Perfil_Parametro.objects.filter(perfil_parametro_state='f')  # Mostrar solo perfiles bloqueados
    return render(request, 'caracterizacion/perfiles_bloqueados.html', {'perfiles_bloqueados': perfiles_bloqueados})

@login_required
def desbloquear_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.perfil_parametro_state = 't'  
    perfil.save()
    return redirect('listar_perfiles_bloqueados')

@login_required
def eliminar_perfil_bloqueado(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.delete()
    return redirect('listar_perfiles_bloqueados')

# Apartado prueba

def listar_pruebas(request, page=None, search=None):
    # Obtenemos el perfil del usuario actual (en caso de necesitarlo para validación)
    profiles = Perfil_Parametro.objects.filter(perfil_parametro_state='t')  # Filtramos los perfiles activos
    # Comprobación para obtener el parámetro `page` de la URL o de la petición GET
    if page is None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')

    # Lógica para manejar la cadena de búsqueda y propagarla a través del paginador
    if search is None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    # Lista vacía para agregar las pruebas que se listarán
    pruebas_all = []
    # Si la búsqueda está vacía o no se encuentra
    if search is None or search.strip() == "" or search == 'NoNe':
        pruebas_array = Prueba.objects.filter(prueba_state='t').order_by('prueba_name')

        for prueba in pruebas_array:
            perfil_parametro = prueba.id_perfil_parametro.perfil_parametro_name
            usuario = prueba.id_user.username
            # Agregamos la información de la prueba
            pruebas_all.append({
                'id': prueba.id,
                'prueba_name': prueba.prueba_name,
                'tipo': prueba.tipo,
                'perfil_parametro': perfil_parametro,
                'usuario': usuario,
                'fecha': prueba.fecha
            })

        paginator = Paginator(pruebas_all, 10)  # Definir `num_elemento` para paginar, aquí asumimos 10 por página
        pruebas_list = paginator.get_page(page)
        template_name = 'caracterizacion/listar_pruebas.html'
        return render(request, template_name, {
            'profiles': profiles,
            'pruebas_list': pruebas_list,
            'paginator': paginator,
            'page': page
        })
    else:
        # Lógica de búsqueda por nombre de prueba o tipo
        pruebas_array = Prueba.objects.filter(
            Q(prueba_name__icontains=search) | Q(tipo__icontains=search)
        ).filter(prueba_state='t').order_by('prueba_name')

        for prueba in pruebas_array:
            perfil_parametro = prueba.id_perfil_parametro.perfil_parametro_name
            usuario = prueba.id_user.username
            # Agregamos la información de la prueba
            pruebas_all.append({
                'id': prueba.id,
                'prueba_name': prueba.prueba_name,
                'tipo': prueba.tipo,
                'perfil_parametro': perfil_parametro,
                'usuario': usuario,
                'fecha': prueba.fecha
            })

    paginator = Paginator(pruebas_all, 10)  # Definir `num_elemento` para paginar, aquí asumimos 10 por página
    pruebas_list = paginator.get_page(page)
    template_name = 'caracterizacion/listar_pruebas.html'
    return render(request, template_name, {
        'profiles': profiles,
        'pruebas_list': pruebas_list,
        'paginator': paginator,
        'page': page,
        'search': search
    })

def detalle_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    mediciones = Medicion.objects.filter(id_prueba=prueba)
    
    context = {
        'prueba_data': prueba,
        'mediciones': mediciones
    }
    
    return render(request, 'caracterizacion/detalle_prueba.html', context)


def editar_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    
    if request.method == 'POST':
        prueba.prueba_name = request.POST.get('prueba_name', prueba.prueba_name)
        prueba.voltaje = request.POST.get('voltaje') or 0.0  # Asigna un valor predeterminado
        prueba.corriente = request.POST.get('corriente') or 0.0
        prueba.resistencia = request.POST.get('resistencia') or 0.0
        prueba.campo = request.POST.get('campo') or 0.0
        
        # Si hay un nuevo archivo de gráfico, actualízalo
        if 'grafico' in request.FILES:
            prueba.grafico = request.FILES['grafico']
            
        prueba.save()

        # Mostrar mensaje de éxito y redirigir
        messages.success(request, 'Prueba actualizada correctamente.')
        return redirect('listar_pruebas')

    return render(request, 'caracterizacion/editar_prueba.html', {'prueba': prueba})

@login_required
def bloquear_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.prueba_state = 'f'  
    prueba.save()
    return redirect('listar_pruebas')  

@login_required
def pruebas_bloqueadas(request):
    pruebas_bloqueadas = Prueba.objects.filter(prueba_state='f')
    return render(request, 'caracterizacion/pruebas_bloqueadas.html', {'pruebas': pruebas_bloqueadas})

@login_required
def desbloquear_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.prueba_state = 't'  
    prueba.save()
    return redirect('pruebas_bloqueadas')

@login_required
def eliminar_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.delete()
    return redirect('pruebas_bloqueadas')

@login_required
def crear_prueba(request):
    if request.method == 'POST':
        perfil_parametro = Perfil_Parametro.objects.get(id=request.POST.get('perfil_parametro'))
        user = User.objects.get(id=request.POST.get('user_id'))
        
        # Crear la Prueba
        nueva_prueba = Prueba.objects.create(
            id_perfil_parametro=perfil_parametro,
            id_user=user,
            prueba_name=request.POST.get('prueba_name'),
            tipo=request.POST.get('tipo'),
            prueba_state='t'
        )
        
        # Crear las Mediciones asociadas
        voltajes = request.POST.getlist('voltaje')
        corrientes = request.POST.getlist('corriente')
        campos = request.POST.getlist('campo')

        for v, c, cm in zip(voltajes, corrientes, campos):
            Medicion.objects.create(
                id_prueba=nueva_prueba,
                voltaje=float(v),
                corriente=float(c),
                campo=float(cm) if cm else None
            )
        
        return redirect('listar_pruebas')  # Redirige a la lista de pruebas después de crearla

    perfiles = Perfil_Parametro.objects.all()
    usuarios = User.objects.all()
    return render(request, 'caracterizacion/crear_prueba.html', {'perfiles': perfiles, 'usuarios': usuarios})