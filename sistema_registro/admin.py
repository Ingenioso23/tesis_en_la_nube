from django.contrib import admin
from .models import RegistroAcceso, SolicitudRestablecimiento
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import CustomUserChangeForm

@admin.register(Usuario)

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Aquí es donde puedes corregir el error
    list_filter = ('is_staff', 'is_superuser', 'groups', 'date_joined')


@admin.register(RegistroAcceso)    
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_hora_acceso', 'resultado_acceso')
    list_filter = ('usuario', 'resultado_acceso')

@admin.register(SolicitudRestablecimiento)
class SolicitudRestablecimientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_solicitud', 'estado')
    list_filter = ('usuario', 'estado')



class CustomUsuarioAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    actions = ['eliminar_usuarios_seleccionados']

    def eliminar_usuarios_seleccionados(self, request, queryset):
        # Acción personalizada para eliminar usuarios seleccionados
        queryset.delete()

    eliminar_usuarios_seleccionados.short_description = "Eliminar usuarios seleccionados"

# Registrar tu modelo de Usuario con el CustomUsuarioAdmin



