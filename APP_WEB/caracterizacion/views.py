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
from .models import Perfil_Parametro, Prueba, Medicion
from .forms import PerfilParametroForm, PruebaForm, MedicionForm


num_elemento = num_pag()#desde core se importa el numero de elementos por página


@login_required
def caracterizacion_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    check_profile_admin(request, profiles)
    template_name = 'caracterizacion/caracterizacion_main.html'
    return render(request,template_name,{'profiles':profiles})
#Flujo usuarios

# Vista para listar todos los perfiles
def perfil_parametro_list(request):
    perfiles = Perfil_Parametro.objects.all()
    return render(request, 'caracterizacion/perfil_parametro_list.html', {'perfiles': perfiles})

# Vista para crear un nuevo perfil
def perfil_parametro_create(request):
    if request.method == 'POST':
        form = PerfilParametroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil_parametro_list')  # Redirigir después de guardar
    else:
        form = PerfilParametroForm()
    return render(request, '', {'form': form})

# Vista para editar un perfil
def perfil_parametro_update(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        form = PerfilParametroForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil_parametro_list')
    else:
        form = PerfilParametroForm(instance=perfil)
    return render(request, '', {'form': form})

# Vista para eliminar un perfil
def perfil_parametro_delete(request, pk):
    perfil = get_object_or_404(Perfil_Parametro, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        return redirect('perfil_parametro_list')
    return render(request, '', {'perfil': perfil})

# Listar todas las pruebas
def prueba_list(request):
    pruebas = Prueba.objects.all()
    return render(request, '', {'pruebas': pruebas})

# Crear una nueva prueba
def prueba_create(request):
    if request.method == 'POST':
        form = PruebaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prueba_list')
    else:
        form = PruebaForm()
    return render(request, '', {'form': form})

# Actualizar una prueba existente
def prueba_update(request, pk):
    prueba = get_object_or_404(Prueba, pk=pk)
    if request.method == 'POST':
        form = PruebaForm(request.POST, request.FILES, instance=prueba)
        if form.is_valid():
            form.save()
            return redirect('prueba_list')
    else:
        form = PruebaForm(instance=prueba)
    return render(request, '', {'form': form})

# Eliminar una prueba
def prueba_delete(request, pk):
    prueba = get_object_or_404(Prueba, pk=pk)
    if request.method == 'POST':
        prueba.delete()
        return redirect('prueba_list')
    return render(request, '', {'object': prueba})


# Listar todas las mediciones
def medicion_list(request):
    mediciones = Medicion.objects.all()
    return render(request, '', {'mediciones': mediciones})

# Crear una nueva medición
def medicion_create(request):
    if request.method == 'POST':
        form = MedicionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicion_list')
    else:
        form = MedicionForm()
    return render(request, '', {'form': form})

# Actualizar una medición existente
def medicion_update(request, pk):
    medicion = get_object_or_404(Medicion, pk=pk)
    if request.method == 'POST':
        form = MedicionForm(request.POST, instance=medicion)
        if form.is_valid():
            form.save()
            return redirect('medicion_list')
    else:
        form = MedicionForm(instance=medicion)
    return render(request, '', {'form': form})

# Eliminar una medición
def medicion_delete(request, pk):
    medicion = get_object_or_404(Medicion, pk=pk)
    if request.method == 'POST':
        medicion.delete()
        return redirect('medicion_list')
    return render(request, '', {'object': medicion})