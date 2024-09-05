from django.shortcuts import render
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

# Create your views here.
def home(request):
    return redirect('login')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def num_pag():
    return 10



@login_required
def pre_check_profile(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()  # Obtener el perfil del usuario
    
    if profile:  # Si el perfil existe
        
        if profile.first_session == 'Si':  # Si es la primera sesión
            print('hola2')
            #profile.first_session = 'No'
            #profile.token_app_session = 'No'
            #profile.save(update_fields=['first_session', 'token_app_session'])  # Guardar cambios en una sola consulta
            return render(request,'registration/password_change_form.html')

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
    
    if profile.group_id in [0,1, 2, 3, 4]:        
        return redirect('admin_main')
    else:
        messages.add_message(request, messages.WARNING, 'No tiene permisos suficientes para acceder a esta área.')
        return redirect('logout')


def check_profile_admin(request,profiles):
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

