"""
URL configuration for FarmaciaInventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Inventario/urls.py
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import include
from django.urls import path

from django.urls import path
from sistema_registro.urls import views
from control_inventarios.urls import views
from control_inventarios import views

if settings.DEBUG:
    import debug_toolbar
 
    urlpatterns = [
    # Otras URLs de tu aplicación
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),  # Página de inicio de sesión
    path('accounts/', include('sistema_registro.urls')),  # Ruta a tus URLs de sistema_registro
    path('accounts/', include('control_inventarios.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('index/', views.index, name='index'),
     
      # Agrega esta línea para el panel de administración
    # Otras URLs de tu aplicación
    ]
