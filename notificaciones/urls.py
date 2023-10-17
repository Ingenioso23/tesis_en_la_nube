# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ... (otras URL)
    path('generar_notificaciones_auto/', views.generar_notificaciones_auto, name='generar_notificaciones_auto'),
    path('generar_notificaciones/', views.generar_notificaciones, name='generar_notificaciones'),
    path('cargar_notificaciones/', views.cargar_notificaciones, name='cargar_notificaciones'),
    
    path('marcar_leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
]