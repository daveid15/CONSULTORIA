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
def listar_perfiles(request):
    perfiles = Perfil_Parametro.objects.all()
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


#PerfilDeCorrienteWeb

def caracterizacion_electrica(request):
    if request.method == 'POST':
        # Aquí puedes manejar los datos del formulario
        nombre = request.POST.get('nombre')
        intervalo_simetrico = request.POST.get('intervalo_simetrico')
        intervalos_corriente = request.POST.get('intervalos_corriente')
        tiempo_medicion = request.POST.get('tiempo_medicion')
        linea_tendencia = request.POST.get('linea_tendencia')

        # Procesar los datos o realizar alguna acción
        # Luego redirigir a una plantilla o página de confirmación
        return render(request, 'caracterizacion_electrica.html', {
            'nombre': nombre,
            'intervalo_simetrico': intervalo_simetrico,
            'intervalos_corriente': intervalos_corriente,
            'tiempo_medicion': tiempo_medicion,
            'linea_tendencia': linea_tendencia,
        })
    else:
        return render(request, 'caracterizacion_electrica.html')


def caracterizacion_magnetoelectrica(request):
    if request.method == 'POST':
        # Obtener datos del formulario enviado
        nombre = request.POST.get('nombre_usuario')
        intervalo_simetrico = request.POST.get('intervalo_simetrico')
        intervalos_corriente = request.POST.get('intervalos_corriente')
        tiempo_medicion = request.POST.get('tiempo_medicion')
        linea_tendencia = request.POST.get('linea_tendencia')
        invertir_polos = request.POST.get('invertir_polos')  # Nuevo checkbox agregado

        # Procesar los datos del formulario
        return render(request, 'caracterizacion_magnetoelectrica.html', {
            'nombre': nombre,
            'intervalo_simetrico': intervalo_simetrico,
            'intervalos_corriente': intervalos_corriente,
            'tiempo_medicion': tiempo_medicion,
            'linea_tendencia': linea_tendencia,
            'invertir_polos': invertir_polos,  # Pasar a la plantilla
        })
    else:
        # Si el método no es POST, simplemente cargar la plantilla sin datos
        return render(request, 'caracterizacion_magnetoelectrica.html')

    