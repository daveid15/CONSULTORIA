
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from caracterizacion import views
from .views import medir_iv_view

caracterizacion_patterns = [
    path('caracterizacion_main', views.caracterizacion_main,name="caracterizacion_main"),
    path('grafico', views.grafico,name="grafico"),
    #flujo usuarios
    path('perfiles/', views.listar_perfiles, name='listar_perfiles'),
    path('perfiles/crear/', views.crear_perfil, name='crear_perfil'),
    path('perfiles/editar/<int:pk>/', views.editar_perfil, name='editar_perfil'),  
    path('perfiles/eliminar/<int:pk>/', views.eliminar_perfil, name='eliminar_perfil'),
    path('perfiles/detalle/<int:pk>/', views.detalle_perfil, name='detalle_perfil'),
<<<<<<< HEAD
<<<<<<< HEAD
=======
    path('medir_iv/', medir_iv_view, name='medir_iv_view'),
>>>>>>> 42f7bc3c2d8354d9016587bdbe25edb4e12af79c
    path('bloquear/<int:perfil_id>/', views.bloquear_perfil, name='bloquear_perfil'),
    path('perfiles_bloqueados/', views.listar_perfiles_bloqueados, name='listar_perfiles_bloqueados'),
    path('desbloquear/<int:perfil_id>/', views.desbloquear_perfil, name='desbloquear_perfil'),
    path('eliminar_bloqueado/<int:perfil_id>/', views.eliminar_perfil_bloqueado, name='eliminar_perfil_bloqueado'),
<<<<<<< HEAD
=======
    path('medir_iv/', medir_iv_view, name='medir_iv_view'),
>>>>>>> 94863ca128b7d6a32e2a90c9ec292f7385266384
=======
>>>>>>> 42f7bc3c2d8354d9016587bdbe25edb4e12af79c
]  