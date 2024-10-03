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

num_elemento = num_pag()#desde core se importa el numero de elementos por página


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

