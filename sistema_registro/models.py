from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

from django.contrib.auth.models import Group


class Usuario(AbstractUser):
    
    
    estado = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='usuarios_group_set')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permission_set')
    

class RegistroAcceso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora_acceso = models.DateTimeField()
    resultado_acceso = models.CharField(max_length=10)  # éxito o falla

class SolicitudRestablecimiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField()
    estado = models.BooleanField(default=True)
