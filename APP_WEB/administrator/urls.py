
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from administrator import views

administrator_patterns = [
    path('admin_main', views.admin_main,name="admin_main"),
    path('new_user/',views.new_user, name='new_user'),

    path('user_block/<user_id>/',views.user_block, name='user_block'),
    path('user_activate/<user_id>',views.user_activate, name='user_activate'),
    path('user_delete/<user_id>',views.user_delete, name='user_delete'),
    
    path('edit_user/<user_id>/',views.edit_user, name='edit_user'),
    path('user_ver/<user_id>/',views.user_ver, name='user_ver'),
    
    path('list_user_active2/',views.list_user_active2, name='list_user_active2'),     
    path('list_user_active2/<groups>/<page>/',views.list_user_active2, name='list_user_active2'),     
    path('list_user_block2/',views.list_user_block2, name='list_user_block2'),     
    path('list_user_block2/<groups>/<page>/',views.list_user_block2, name='list_user_block2'), 
    
    path('carga_masiva/',views.carga_masiva,name="carga_masiva"),# administrador_carga_masiva
    path('carga_masiva_save/',views.carga_masiva_save,name="carga_masiva_save"),#administrador_carga_masiva_save
    path('import_administrator/',views.import_administrator,name="import_administrator"),#administrador
    path('administrator/carga_masiva/',views.carga_masiva,name="carga_masiva"),#administrador
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard")]  