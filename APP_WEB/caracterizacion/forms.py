from django import forms
from .models import Perfil_Parametro, Prueba, Medicion

class PerfilParametroForm(forms.ModelForm):
    class Meta:
        model = Perfil_Parametro
        fields = '__all__'  

class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = '__all__'

class MedicionForm(forms.ModelForm):
    class Meta:
        model = Medicion
        fields = '__all__'
