# Generated by Django 4.2.6 on 2023-10-17 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0002_notificacion_mostrada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacion',
            name='mostrada',
        ),
    ]
