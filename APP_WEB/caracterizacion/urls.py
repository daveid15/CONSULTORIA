
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from caracterizacion import views

caracterizacion_patterns = [
    path('caracterizacion_main', views.caracterizacion_main,name="caracterizacion_main"),
    #flujo usuarios
    path('perfiles/', views.listar_perfiles, name='listar_perfiles'),
    path('perfiles/crear/', views.crear_perfil, name='crear_perfil'),
    path('perfiles/editar/<int:pk>/', views.editar_perfil, name='editar_perfil'),
    path('perfiles/eliminar/<int:pk>/', views.eliminar_perfil, name='eliminar_perfil'),
    path('perfiles/detalle/<int:pk>/', views.detalle_perfil, name='detalle_perfil'),
    path('bloquear/<int:perfil_id>/', views.bloquear_perfil, name='bloquear_perfil'),
    path('perfiles_bloqueados/', views.listar_perfiles_bloqueados, name='listar_perfiles_bloqueados'),
    path('eliminar_bloqueado/<int:perfil_id>/', views.eliminar_perfil_bloqueado, name='eliminar_perfil_bloqueado'),
]  