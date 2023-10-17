# views.py
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F
from .models import Notificacion
from control_inventarios.models import Producto
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.utils import timezone
from datetime import timedelta
logger = logging.getLogger(__name__)

@csrf_exempt
def generar_notificaciones_auto(request):
    try:
        # Llamando a la función de generación de notificaciones
        generar_notificaciones(request)
        return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
    except Exception as e:
        # Registrando cualquier excepción que ocurra
        logger.error(f"Error en la generación automática de notificaciones: {e}")
        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')

def generar_notificaciones(request):
    logger.info("Inicio de generar_notificaciones")
    
    # Obtener productos con cantidadstock por debajo o igual a NivelReorden
    productos_bajos_stock = Producto.objects.filter(CantidadStock__lte=F('NivelReorden'))
    
    for producto in productos_bajos_stock:
        # Verificar si ya existe una notificación para este producto
        notificacion_existente = Notificacion.objects.filter(
            mensaje__contains=producto.NombreProducto,
        ).first()

        if not notificacion_existente or not notificacion_existente.leida:
            # Eliminar notificaciones existentes para este producto
            Notificacion.objects.filter(mensaje__contains=producto.NombreProducto).delete()

            # Generar una nueva notificación
            mensaje = f"El producto {producto.NombreProducto} tiene un nivel bajo de stock. Cantidad actual: {producto.CantidadStock}"
            notificacion = Notificacion.objects.create(mensaje=mensaje)
            logger.info(f"Notificación creada: {mensaje}")

    logger.info("Fin de generar_notificaciones")
    return render(request, 'notificaciones.html')

def cargar_notificaciones(request):
    # Obtener las notificaciones no leídas
    notificaciones = Notificacion.objects.filter(leida=False).order_by('-fecha_creacion')[:5]
    notificaciones_data = [{'id': notif.id, 'mensaje': notif.mensaje, 'fecha_creacion': notif.fecha_creacion, 'leida': notif.leida} for notif in notificaciones]

    # Devolver los datos en la respuesta JSON
    return JsonResponse({'notificaciones': notificaciones_data}, safe=False)

def marcar_notificacion_leida(request, notificacion_id):
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.leida = 1
    notificacion.save()

    notificaciones_no_leidas = Notificacion.objects.filter(leida=False).count()

    return JsonResponse({'notificaciones': notificaciones_no_leidas})
