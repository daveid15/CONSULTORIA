#from django.shortcuts import render
from django.conf import settings #importa el archivo settings
from django.contrib import messages #habilita la mesajería entre vistas
from django.contrib.auth.decorators import login_required #habilita el decorador que se niega el acceso a una función si no se esta logeado
from django.contrib.auth.models import Group, User # importa los models de usuarios y grupos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #permite la paqinación
from django.db.models import Avg, Count, Q #agrega funcionalidades de agregación a nuestros QuerySets
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect) #Salidas alternativas al flujo de la aplicación se explicará mas adelante
from django.shortcuts import redirect, render #permite renderizar vistas basadas en funciones o redireccionar a otras funciones
from django.template import RequestContext # contexto del sistema
from django.views.decorators.csrf import csrf_exempt #decorador que nos permitira realizar conexiones csrf
from registration.models import Profile #importa el modelo profile, el que usaremos para los perfiles de usuarios
from caracterizacion.models import Perfil_Parametro,Prueba, Medicion

# Create your views here.
def home(request):
    return redirect('login')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash, logout
#from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


def num_pag():
    return 1



@login_required
def pre_check_profile(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()  # Obtener el perfil del usuario
    
    if profile:  # Si el perfil existe
        
        if profile.first_session == 'Si':  # Si es la primera sesión
            return render(request,'registration/password_change_form.html')
        else:
            # Si no es la primera sesión, redirigir al dashboard principal
            # Verificar el atributo group_id para redirigir al usuario según su rol
            if profile.group_id == 1:  # Administrador
                print("hola")
                return redirect('admin_main')
            elif profile.group_id == 2:  # Usuario común
                print("hola2")
                return redirect('listar_perfiles')
            else:
                # Redirigir a una página por defecto si el group_id no coincide
                messages.add_message(request, messages.WARNING, 'Grupo no reconocido.')
                return redirect('login')
    else:
        messages.add_message(request, messages.INFO, 'Perfil no encontrado. Por favor, contacte al administrador.')
        return redirect('login')
    
    return redirect('login')  # Redirigir a una vista predeterminada si no se cumple ninguna condición


def check_profile(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Hubo un error con su usuario, por favor contactese con los administradores')              
        return redirect('login')
    
    if profile.group_id in [1]:        
        return redirect('admin_main')
    else:
        messages.add_message(request, messages.WARNING, 'No tiene permisos suficientes para acceder a esta área.')
        return redirect('logout')


def check_profile_admin(request,profiles):
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('listar_perfiles')
        








