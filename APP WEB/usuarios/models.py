from django.db import models

# Create your models here.

class Persona(models.Model):
    PERFIL_CHOICES = [
        ('AC', 'Académico'),
        ('ES', 'Estudiante'),
    ]
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    perfil = models.CharField(max_length=2, choices=PERFIL_CHOICES)

    def __str__(self):
        return f"{self.nombre}"
