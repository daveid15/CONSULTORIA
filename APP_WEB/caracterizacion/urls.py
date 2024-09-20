
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from caracterizacion import views

caracterizacion_patterns = [
    path('caracterizacion_main', views.caracterizacion_main,name="caracterizacion_main"),
    #flujo usuarios
    path('perfiles/', views.perfil_parametro_list, name='perfil_parametro_list'),
    path('perfiles/nuevo/', views.perfil_parametro_create, name='perfil_parametro_create'),
    path('perfiles/<int:pk>/editar/', views.perfil_parametro_update, name='perfil_parametro_update'),
    path('perfiles/<int:pk>/eliminar/', views.perfil_parametro_delete, name='perfil_parametro_delete'),
]  