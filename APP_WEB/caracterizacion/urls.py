
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from caracterizacion import views

caracterizacion_patterns = [
    path('caracterizacion_main', views.caracterizacion_main,name="caracterizacion_main"),
    path('grafico', views.grafico,name="grafico"),
    #flujo usuarios
]  