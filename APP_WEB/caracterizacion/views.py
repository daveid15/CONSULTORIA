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
from rest_framework import generics,status
from .serializers import PerfilParametroSerializer, PruebaSerializer, MedicionSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class PerfilParametroListAPIView(generics.ListAPIView):
    queryset = Perfil_Parametro.objects.all()
    serializer_class = PerfilParametroSerializer

# Para manejar Prueba
class PruebaCreateAPIView(generics.CreateAPIView):
    queryset = Prueba.objects.all()
    serializer_class = PruebaSerializer

class PruebaListAPIView(generics.ListAPIView):
    queryset = Prueba.objects.all()
    serializer_class = PruebaSerializer

# Para manejar Medicion
class MedicionCreateAPIView(generics.CreateAPIView):
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer

class MedicionListAPIView(generics.ListAPIView):
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer

class PerfilParametroCreateAPIView(generics.CreateAPIView):
    queryset = Perfil_Parametro.objects.all()
    serializer_class = PerfilParametroSerializer

    def create(self, request, *args, **kwargs):
        # Obtener el nombre del perfil de parámetro desde el request
        perfil_parametro_name = request.data.get('perfil_parametro_name', None)
        
        # Verificar si el perfil de parámetro ya existe
        perfil_parametro = Perfil_Parametro.objects.filter(perfil_parametro_name=perfil_parametro_name).first()
        
        if perfil_parametro:
            # Si el perfil ya existe, no lo creamos, solo usamos el existente
            # Puedes devolver un mensaje indicando que se usará el perfil existente si lo deseas
            serializer = self.get_serializer(perfil_parametro)
            pass
        else:
            # Si no existe, crear el nuevo perfil de parámetro
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fija_corriente = request.data.get('fija_corriente', None)  # Valor predeterminado None si no se pasa
            perfil_parametro = serializer.save(fija_corriente=fija_corriente)

        # Obtener datos para pruebas y mediciones del request
        pruebas_data = request.data.get('pruebas', [])  # Lista de pruebas

        for prueba_data in pruebas_data:
            # Crear cada prueba relacionada al perfil existente
            user = User.objects.first()  # Cambia según tu lógica

            # Obtener los valores de pendiente, intercepto, y configuración_rele desde la solicitud
            pendiente = prueba_data.get('pendiente', 0.0)
            intercepto = prueba_data.get('intercepto', 0.0)
            configuracion_rele = prueba_data.get('configuracion_rele', '')

            prueba = Prueba.objects.create(
                id_perfil_parametro=perfil_parametro,
                id_user=user,
                prueba_name=prueba_data.get('prueba_name', f"Prueba de {perfil_parametro.perfil_parametro_name}"),
                tipo=prueba_data.get('tipo', 'Automática'),
                pendiente=pendiente,  # Almacenar pendiente
                intercepto=intercepto,  # Almacenar intercepto
                configuracion_rele=configuracion_rele  # Almacenar configuracion_rele
            )

            # Crear las mediciones asociadas a cada prueba
            mediciones_data = prueba_data.get('mediciones', [])  # Lista de mediciones
            for medicion_data in mediciones_data:
                # Obtener los valores de campo, delta_v, y saturacion_campo desde la medición
                campo = medicion_data.get('campo', 0.0)
                delta_v = medicion_data.get('delta_v', 0.0)
                saturacion_campo = medicion_data.get('saturacion_campo', 0.0)

                Medicion.objects.create(
                    id_prueba=prueba,
                    voltaje=medicion_data.get('voltaje', 0.0),
                    corriente=medicion_data.get('corriente', 0.0),
                    resistencia=0.0,  # Se calculará automáticamente en `save()`
                    campo=campo,  # Almacenar campo
                    delta_v=delta_v,  # Almacenar delta_v
                    saturacion_campo=saturacion_campo  # Almacenar saturacion_campo
                )


        return Response(serializer.data, status=status.HTTP_201_CREATED)


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



def medir_iv_view(request, id_medicion):
    profiles = Profile.objects.get(user_id = request.user.id)
    mediciones = Medicion.objects.filter(pk = id_medicion)
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
def listar_perfiles(request):
    # Filtrar solo perfiles activos
    perfiles = Perfil_Parametro.objects.filter(perfil_parametro_state='t').order_by('perfil_parametro_name')

    # Configuración de paginación: 10 perfiles por página
    page = request.GET.get('page', 1)  # Obtiene el número de página desde los parámetros GET
    paginator = Paginator(perfiles, 5)  # Limitar a 10 perfiles por página
    perfiles_list = paginator.get_page(page)

    # Contexto para el template
    context = {
        'perfiles_list': perfiles_list,
        'paginator': paginator,
    }

    return render(request, 'caracterizacion/listar_perfiles.html', context)

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
    # Obtener solo los perfiles bloqueados
    perfiles_bloqueados = Perfil_Parametro.objects.filter(perfil_parametro_state='f')
    
    # Configurar la paginación
    page = request.GET.get('page', 1)  # Obtener la página actual desde la URL (por defecto, página 1)
    paginator = Paginator(perfiles_bloqueados, 5)  # Limitar a 5 perfiles por página
    perfiles_bloqueados_list = paginator.get_page(page)  # Obtener los perfiles para la página actual

    # Contexto para el template
    context = {
        'perfiles_bloqueados_list': perfiles_bloqueados_list,  # Lista de perfiles bloqueados paginada
        'paginator': paginator,  # El objeto del paginador
    }

    return render(request, 'caracterizacion/perfiles_bloqueados.html', context)

@login_required
def desbloquear_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil_Parametro, id=perfil_id)
    perfil.perfil_parametro_state = 't'
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

        paginator = Paginator(pruebas_all, 5)  #5 por página
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

    paginator = Paginator(pruebas_all, 5)  # Definir `num_elemento` para paginar, aquí asumimos 10 por página
    pruebas_list = paginator.get_page(page)
    template_name = 'caracterizacion/listar_pruebas.html'
    return render(request, template_name, {
        'profiles': profiles,
        'pruebas_list': pruebas_list,
        'paginator': paginator,
        'page': page,
        'search': search
    })

def detalle_prueba(request, prueba_id, page=None):
    # Obtener la prueba y el perfil de parámetro asociado
    prueba = get_object_or_404(Prueba, id=prueba_id)
    perfil_parametro = prueba.id_perfil_parametro  # Suponiendo que la prueba tiene un perfil de parámetro relacionado

    # Obtener todas las mediciones relacionadas con la prueba
    mediciones = Medicion.objects.filter(id_prueba=prueba).order_by('fecha')  # Ordenar por fecha o como prefieras

    # Configurar la paginación
    if page is None:
        page = request.GET.get('page')  # Obtener la página de la URL si no se pasa como argumento

    paginator = Paginator(mediciones, 1)  # Limitar a 10 mediciones por página
    mediciones_list = paginator.get_page(page)

    # Contexto para el template
    context = {
        'prueba': prueba,
        'perfil_parametro': perfil_parametro,
        'mediciones_list': mediciones_list,
        'paginator': paginator,
        'page': page,
    }
    
    return render(request, 'caracterizacion/detalle_prueba.html', context)


@login_required
def bloquear_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.prueba_state = 'f'  
    prueba.save()
    return redirect('listar_pruebas')  

def listar_pruebas_bloqueadas(request):
    # Filtrar solo las pruebas bloqueadas
    pruebas_bloqueadas = Prueba.objects.filter(prueba_state='f')  # Mostrar solo pruebas bloqueadas

    # Configurar la paginación
    page = request.GET.get('page', 1)  # Obtener el número de página desde la URL
    paginator = Paginator(pruebas_bloqueadas, 5)  # Mostrar 5 pruebas por página
    pruebas_bloqueadas_list = paginator.get_page(page)

    # Pasar los datos al contexto
    context = {
        'pruebas_bloqueadas_list': pruebas_bloqueadas_list,
        'paginator': paginator
    }

    return render(request, 'caracterizacion/pruebas_bloqueadas.html', context)


@login_required
def desbloquear_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.prueba_state = 't'  
    prueba.save()
    return redirect('pruebas_bloqueadas')

@login_required
def eliminar_prueba_bloqueada(request, prueba_id):
    prueba = get_object_or_404(Prueba, id=prueba_id)
    prueba.delete()
    return redirect('pruebas_bloqueadas')

@login_required
def mostrar_grafico(request, prueba_id):
    # Obtener la prueba, o mostrar un error 404 si no existe
    prueba = get_object_or_404(Prueba, id=prueba_id)
    perfil_parametro = prueba.id_perfil_parametro
    # Filtrar mediciones asociadas a la prueba
    mediciones = Medicion.objects.filter(id_prueba=prueba_id)

    # Si no hay mediciones, lanzar una excepción o mostrar un mensaje en el template
    if not mediciones:
        raise Http404("No se encontraron mediciones para esta prueba.")

    # Generar listas de corriente y voltaje
    array_current = [medicion.corriente for medicion in mediciones]
    array_voltaje = [medicion.voltaje for medicion in mediciones]

    # Preparar los datos para el template
    template_name = 'caracterizacion/mostrar_grafico.html'
    return render(request, template_name, {
        'prueba': prueba,
        'perfil_parametro': perfil_parametro,
        'currents': array_current,
        'volts': array_voltaje,
        'num_mediciones': len(array_current)  # Opcional: para mostrar la cantidad de puntos
    })

@login_required
def descargar_datos(request, prueba_id):
    prueba = Prueba.objects.get(id=prueba_id)
    mediciones = Medicion.objects.filter(id_prueba=prueba_id)

    # Crear contenido del archivo .txt
    contenido = f"Prueba: {prueba.prueba_name}\n\nPerfil de Parámetro Asociado:\n"
    contenido += f"ID del Perfil: {prueba.id_perfil_parametro.id}\n"
    contenido += f"Nombre del Perfil: {prueba.id_perfil_parametro.perfil_parametro_name}\n"
    contenido += "\nMediciones:\nCorriente (A) \t Voltaje (V)\n"

    for medicion in mediciones:
        contenido += f"{medicion.corriente}\t{medicion.voltaje}\n"

    # Crear y devolver el archivo .txt como respuesta
    response = HttpResponse(contenido, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="detalle_prueba_{prueba.prueba_name}.txt"'
    return response
