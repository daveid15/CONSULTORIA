from rest_framework import serializers
from .models import Perfil_Parametro, Prueba, Medicion

class PerfilParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil_Parametro
        fields = '__all__'  # O especifica los campos que deseas incluir

class PruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        fields = '__all__'  # O especifica los campos que deseas incluir

class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = '__all__'  # O especifica los campos que deseas incluir
