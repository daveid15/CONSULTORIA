
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from caracterizacion import views
from .views import (
    medir_iv_view,
    PerfilParametroCreateAPIView,
    PerfilParametroListAPIView,
    PruebaCreateAPIView,
    PruebaListAPIView,
    MedicionCreateAPIView,
    MedicionListAPIView
)

caracterizacion_patterns = [
    path('caracterizacion_main', views.caracterizacion_main,name="caracterizacion_main"),
    path('grafico', views.grafico,name="grafico"),
    #flujo usuarios
    path('perfiles/', views.listar_perfiles, name='listar_perfiles'),
    path('perfiles/crear/', views.crear_perfil, name='crear_perfil'),
    path('perfiles/editar/<int:pk>/', views.editar_perfil, name='editar_perfil'),  
    path('perfiles/eliminar/<int:pk>/', views.eliminar_perfil, name='eliminar_perfil'),
    path('perfiles/detalle/<int:pk>/', views.detalle_perfil, name='detalle_perfil'),
    path('medir_iv/', medir_iv_view, name='medir_iv_view'),
    path('bloquear/<int:perfil_id>/', views.bloquear_perfil, name='bloquear_perfil'),
    path('perfiles_bloqueados/', views.listar_perfiles_bloqueados, name='listar_perfiles_bloqueados'),
    path('desbloquear/<int:perfil_id>/', views.desbloquear_perfil, name='desbloquear_perfil'),
    path('eliminar_bloqueado/<int:perfil_id>/', views.eliminar_perfil_bloqueado, name='eliminar_perfil_bloqueado'),
    
    path('pruebas/', views.listar_pruebas, name='listar_pruebas'),
    path('pruebas/detalle/<int:prueba_id>/', views.detalle_prueba, name='detalle_prueba'),
    path('pruebas/bloquear/<int:prueba_id>/', views.bloquear_prueba, name='bloquear_prueba'),
    path('pruebas_bloqueadas/', views.listar_pruebas_bloqueadas, name='pruebas_bloqueadas'),
    path('pruebas/desbloquear/<int:prueba_id>/', views.desbloquear_prueba, name='desbloquear_prueba'),
    path('mostrar_grafico/<int:prueba_id>/', views.mostrar_grafico, name='mostrar_grafico'),
    path('descargar_datos/<int:prueba_id>/', views.descargar_datos, name='descargar_datos'),
    path('pruebas/eliminar_prueba_bloqueado/<int:prueba_id>/', views.eliminar_prueba_bloqueada, name='eliminar_prueba_bloqueada'),
    path('perfil/<int:perfil_id>/pruebas/', views.listar_pruebas_perfil, name='listar_pruebas_perfil')
    path('pruebas/eliminar_prueba_bloqueado/<int:prueba_id>/', views.eliminar_prueba_bloqueada, name='eliminar_prueba_bloqueada'),

    #API
    path('api_parametro/', PerfilParametroCreateAPIView.as_view(), name='perfil-parametro-create'),
    path('api_parametros/', PerfilParametroListAPIView.as_view(), name='perfil-parametro-list'),
    
    path('api_prueba/', PruebaCreateAPIView.as_view(), name='prueba-create'),
    path('api_pruebas/', PruebaListAPIView.as_view(), name='prueba-list'),

    path('api_medicion/', MedicionCreateAPIView.as_view(), name='medicion-create'),
    path('api_mediciones/', MedicionListAPIView.as_view(), name='medicion-list'),
]  