from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate
from django.contrib import admin
from registration import views

urlpatterns = [
    path('ejemplos_correo1/',views.ejemplos_correo1,name="ejemplos_correo1"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileUpdate.as_view(), name="profile"),  
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),       
    path('profile_edit/', views.profile_edit, name='profile_edit'), 
    

]
