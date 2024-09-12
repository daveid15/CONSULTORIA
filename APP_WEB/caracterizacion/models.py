from django.db import models

# Create your models here.
class Perfil_Parametro(models.Model):
    
    rut_proveedor = models.CharField(max_length = 100,null=True, blank=True) 
    nombre_proveedor = models.CharField(max_length = 100,null=True, blank=True)  
    correo_proveedor = models.CharField(max_length = 100,null=True, blank=True)  
    telefono_proveedor = models.IntegerField(null=True, blank=True)
    perfil_parametro_state = models.CharField(max_length=10, null=True, blank=True, default='t')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_proveedor']
    
    def __str__(self):
        return self.nombre_proveedor