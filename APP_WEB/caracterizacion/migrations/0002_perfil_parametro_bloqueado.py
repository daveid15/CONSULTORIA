# Generated by Django 2.0.2 on 2024-09-30 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caracterizacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil_parametro',
            name='bloqueado',
            field=models.BooleanField(default=False),
        ),
    ]
