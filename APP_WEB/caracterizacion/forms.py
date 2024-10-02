from django import forms
from .models import Perfil_Parametro

class PerfilParametroForm(forms.ModelForm):
    class Meta:
        model = Perfil_Parametro
        fields = ['perfil_parametro_name', 'intervalo_simetrico', 'intervalo_corriente', 'delay']


