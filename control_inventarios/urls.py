# En urls.py de tu aplicación

from django.urls import path
from . import views
from .views import borrar_entidad_salud, consultar_entradas, consultar_salidas, detalle_entidad_salud, editar_entidad_salud, exportar_entradas, exportar_salidas, lista_entidades_salud

from .views import editar_producto
urlpatterns = [
    path('registrar_entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('entrada_exitosa/', views.entrada_exitosa, name='entrada_exitosa'),
    path('salida_exitosa/', views.salida_exitosa, name='salida_exitosa'),
    path('index/', views.index, name='index'),
    path('visualizar_inventario/', views.visualizar_inventario, name='visualizar_inventario'),
    path('registrar_entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('productos/', views.productos, name='productos'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('eliminar_producto/<str:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('editar_producto/<str:pk>/', views.editar_producto, name='editar_producto'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('editar_cliente/<str:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('borrar_cliente/<str:id_cliente>/', views.borrar_cliente, name='borrar_cliente'),
    path('clientes/', views.clientes, name='clientes'),  # La URL y la vista asociada
    path('entidades/', views.entidades, name='entidades'),
    #path('lista_entidades_salud/<str:id_entidad>/', lista_entidades_salud, name='lista_entidades_salud'),
    path('lista_entidades_salud/', lista_entidades_salud, name='lista_entidades_salud'),
    path('detalle_entidad_salud/<str:id_entidad>/', detalle_entidad_salud, name='detalle_entidad_salud'),
    path('crear_entidad_salud/', views.crear_entidad_salud, name='crear_entidad_salud'),
    path('editar_entidad_salud/<str:id_entidad>/', editar_entidad_salud, name='editar_entidad_salud'),
    path('borrar_entidad_salud/<str:id_entidad>/', borrar_entidad_salud, name='borrar_entidad_salud'),
    path('registrar-salida/', views.registrar_salida, name='registrar_salida'),
    path('inventario_data/', views.inventario_data, name='inventario_data'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/<str:id_proveedor>/', views.editar_proveedor, name='editar_proveedor'),
    path('borrar_proveedor/<str:id_proveedor>/', views.borrar_proveedor, name='borrar_proveedor'),
    path('proveedor/', views.proveedor, name='proveedor'),
    
    path('exportar_entradas/', exportar_entradas, name='exportar_entradas'),
    path('exportar_salidas/', exportar_salidas, name='exportar_salidas'),
    path('consultar_entradas/', consultar_entradas, name='consultar_entradas'),
    path('consultar_salidas/', consultar_salidas, name='consultar_salidas'),
    
    #path('notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),

]
