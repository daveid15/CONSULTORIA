# Generated by Django 2.0.2 on 2024-10-04 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caracterizacion', '0002_perfil_parametro_bloqueado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil_parametro',
            name='perfil_parametro_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
