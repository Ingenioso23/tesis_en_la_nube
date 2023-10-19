from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    estado = models.BooleanField(default=True)

class RegistroAcceso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora_acceso = models.DateTimeField()
    resultado_acceso = models.CharField(max_length=10) # éxito o falla

class SolicitudRestablecimiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField()
    fecha_restablecimiento = models.DateTimeField(null=True, blank=True)