from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import  User
class Perfil_Parametro(models.Model):
    perfil_parametro_name = models.CharField(max_length = 100,unique=True)
    #Este toma el valor de intervalo simetrico o saturacion de campo
    intervalo_simetrico = models.FloatField(
        # La corriente debe estar entre 1.05A y -1.05A
        validators=[MinValueValidator(-1.05), MaxValueValidator(1.05)],
        null=False,
        blank=False
    )
    #Este toma el valor de intervalo de corriente o intervalos de corrientes
    intervalo_corriente = models.IntegerField(null=False, blank= False)
    delay = models.FloatField(
        #delay entre intervalo de corriente debe estar entre 0.001s y 999.999s
        validators=[MinValueValidator(0.001), MaxValueValidator(999.999)],
        null=False,
        blank= False
    )
    perfil_parametro_state = models.CharField(max_length=10, null=True, blank=True, default='t')
    
    bloqueado = models.BooleanField(default=False)
    
    fija_corriente = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Perfil Parametro'
        verbose_name_plural = 'Perfil Parametros'
        ordering = ['perfil_parametro_name']
    
    def __str__(self):
        return self.perfil_parametro_name
    
    
class Prueba (models.Model):
    id_perfil_parametro = models.ForeignKey(Perfil_Parametro, on_delete=models.CASCADE, null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    prueba_name = models.CharField(max_length= 255, null= False, blank= True)
    tipo = models.CharField(max_length= 255, null= False,blank=False)
    grafico = models.ImageField(null=True, blank= True)
    fecha = models.DateTimeField(auto_now=True)
    prueba_state = models.CharField(max_length=10, null=False, blank=False, default='t')
    pendiente= models.FloatField(null=True, blank=True)
    intercepto = models.FloatField(null=True, blank=True)
    configuracion_rele = models.CharField(max_length= 255, null= True, blank= True)
    #True, false, false, true

    
    
    class Meta:
        verbose_name = 'Prueba'
        verbose_name_plural = 'Pruebas'
        ordering = ['prueba_name']
    
    def __str__(self):
        return self.prueba_name


class Medicion(models.Model):
    id_prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, null=False, blank=False)
    voltaje = models.FloatField(null=False, blank=False)
    corriente = models.FloatField(null=False, blank=False)
    resistencia = models.FloatField(null=False, blank=False)
    campo = models.FloatField(null=True, blank=True)
    saturacion_campo = models.FloatField(null=True, blank=True)
    delta_v = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.voltaje is not None and self.corriente is not None and self.corriente != 0:
            self.resistencia = self.voltaje / self.corriente
        super().save(*args, **kwargs) 

    class Meta:
        verbose_name = 'Medición'
        verbose_name_plural = 'Mediciones'
        ordering = ['corriente']
    
    def __str__(self):
        return str(self.corriente)