# Generated by Django 5.1.7 on 2025-04-03 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_alter_pelicula_sala'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='sala',
            field=models.ForeignKey(blank=True, default=10, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='peliculas', to='usuarios.sala'),
        ),
    ]
