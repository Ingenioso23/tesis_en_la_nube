# decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def is_nuevo_empleado(user):
    return user.groups.filter(name='Nuevo Empleado').exists()

def is_usuario_registrado(user):
    return user.groups.filter(name='Usuario Registrado').exists()

def is_personal_ipsi(user):
    return user.groups.filter(name='Personal de IPSI').exists()

def is_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def is_administrador(user):
    return user.groups.filter(name='Administrador').exists()

def decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        test_result = request.user.is_authenticated and (request.user.groups.filter(name='Administrador').exists() or request.user.groups.filter(name='usuario_registrado').exists())
        
        if not test_result:
            return redirect('index')  # Ajusta el nombre de la vista de login
            
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def group_required(group_name):
    def check_group(user):
        return user.groups.filter(name=group_name).exists()

    return user_passes_test(check_group, login_url='login')
