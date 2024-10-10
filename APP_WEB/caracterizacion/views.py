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


num_elemento = num_pag()#desde core se importa el numero de elementos por página


@login_required
def caracterizacion_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    check_profile_admin(request, profiles)
    template_name = 'caracterizacion/caracterizacion_main.html'
    return render(request,template_name,{'profiles':profiles})
#Flujo usuarios

# Listar perfiles de parámetros
@login_required
def listar_perfiles(request):
    #perfiles = Perfil_Parametro.objects.all()
    perfiles = Perfil_Parametro.objects.filter(perfil_parametro_state='t')  # Mostrar solo perfiles activos
    return render(request, 'caracterizacion/listar_perfiles.html', {'perfiles': perfiles})

# Crear un perfil de parámetros 
@login_required
def crear_editar_perfil(request, pk=None):
    if pk:  # Si pk está presente, estamos en modo edición
        perfil = get_object_or_404(Perfil_Parametro, pk=pk)
        es_editar = True
    else:  # Si pk no está presente, estamos en modo creación
        perfil = None
        es_editar = False

    if request.method == 'POST':
        nombre_perfil = request.POST.get('perfil_parametro_name')
        intervalo_simetrico = request.POST.get('intervalo_simetrico')
        intervalo_corriente = request.POST.get('intervalo_corriente')
        delay = request.POST.get('delay')
        estado = request.POST.get('perfil_parametro_state', 't')

        
        intervalo_simetrico = float(intervalo_simetrico) if intervalo_simetrico else None
        intervalo_corriente = float(intervalo_corriente) if intervalo_corriente else None
        delay = float(delay) if delay else None

        # Si estamos en modo edición, actualizamos el perfil existente
        if es_editar:
            perfil.perfil_parametro_name = nombre_perfil
            perfil.intervalo_simetrico = intervalo_simetrico
            perfil.intervalo_corriente = intervalo_corriente
            perfil.delay = delay
            perfil.perfil_parametro_state = estado
            perfil.save()
            return redirect('listar_perfiles')

        # Si estamos en modo creación, creamos un nuevo perfil
        else:
            nuevo_perfil = Perfil_Parametro(
                perfil_parametro_name=nombre_perfil,
                intervalo_simetrico=intervalo_simetrico,
                intervalo_corriente=intervalo_corriente,
                delay=delay,
                perfil_parametro_state=estado
            )
            nuevo_perfil.save()
            return redirect('listar_perfiles')

    # Si es GET, mostrar el formulario con o sin datos (en caso de edición)
    return render(request, 'caracterizacion/crear_editar_perfil.html', {
        'perfil': perfil,
        'es_editar': es_editar
    })


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
    perfil.bloqueado = False
    perfil.save()
    return redirect('listar_perfiles_bloqueados')

@login_required
def eliminar_perfil_bloqueado(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.delete()
    return redirect('listar_perfiles_bloqueados')

# Apartado prueba
@login_required
def crear_editar_prueba(request, pk=None):
    if pk:  # Modo edición
        prueba = get_object_or_404(Prueba, pk=pk)
        es_editar = True
    else:  # Modo creación
        prueba = None
        es_editar = False

    if request.method == 'POST':
        nombre_prueba = request.POST.get('prueba_name')
        tipo = request.POST.get('tipo')
        grafico = request.FILES.get('grafico')
        prueba_state = request.POST.get('prueba_state', 't')

        # Validar si el nombre ya existe al crear una nueva prueba
        if not es_editar and Prueba.objects.filter(prueba_name=nombre_prueba).exists():
            error_message = "El nombre de la prueba ya existe. Por favor, elija otro."
            return render(request, 'caracterizacion/crear_editar_prueba.html', {
                'error_message': error_message,
                'prueba': prueba
            })

        # Actualización de la prueba en modo edición
        if es_editar:
            prueba.prueba_name = nombre_prueba
            prueba.tipo = tipo
            if grafico:  # Solo actualiza el gráfico si se proporciona uno nuevo
                prueba.grafico = grafico
            prueba.prueba_state = prueba_state
            prueba.save()
            return redirect('listar_pruebas')

        # Creación de una nueva prueba
        else:
            nueva_prueba = Prueba(
                prueba_name=nombre_prueba,
                tipo=tipo,
                grafico=grafico,
                prueba_state=prueba_state
            )
            nueva_prueba.save()
            return redirect('listar_pruebas')

    return render(request, 'caracterizacion/crear_editar_prueba.html', {
        'prueba': prueba,
        'es_editar': es_editar
    })

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