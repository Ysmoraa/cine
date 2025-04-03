# Generated by Django 5.1.7 on 2025-04-03 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_genero_alter_usuario_tipo_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelicula',
            name='sala',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='peliculas', to='usuarios.sala'),
        ),
    ]
