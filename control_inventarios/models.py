# En models.py

from django.db import models
from notifications.signals import notify
from django.db.models import F

class EntidadSalud(models.Model):
    id_entidad = models.CharField(primary_key=True, max_length=13, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    TIPOCLIENTES = (
        ('Interno', 'Interno'),
        ('Externo', 'Externo'),
    )
    id_cliente = models.CharField(primary_key=True, max_length=13, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    tipo_cliente = models.CharField(max_length=255, choices=TIPOCLIENTES)
    entidad_salud = models.ForeignKey(EntidadSalud, on_delete=models.SET_NULL, blank=True, null=True)  # Relación con entidad de salud

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    id_proveedor = models.CharField(primary_key=True, max_length=13, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    CATEGORIAS = (
        ('Medicamento', 'Medicamento'),
        ('Suministro', 'Suministro'),
    )

    id = models.CharField(primary_key=True, max_length=8, null=False)
    NombreProducto = models.CharField(max_length=255, null=False)
    categoria = models.CharField(max_length=255, choices=CATEGORIAS, null=False)
    TipoProducto = models.CharField(max_length=255, null=False)
    Concentracion = models.CharField(max_length=255)
    FormaFarmaceutica = models.CharField(max_length=255)
    UnidadesMedida = models.CharField(max_length=255, null=False)
    NumeroLote = models.CharField(max_length=255)
    FechaVencimiento = models.DateField(default=None, null=False)
    CantidadStock = models.IntegerField(default=0, null=False)
    NivelReorden = models.IntegerField(default=0, null=False)
    Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    NumeroReferencia = models.CharField(max_length=255)
    UbicacionAlmacen = models.CharField(max_length=255, null=False)
    
    
    def actualizar_stock(self, cantidad):
        # Actualizar la cantidad de stock descontando la cantidad especificada
        Producto.objects.filter(id=self.id).update(CantidadStock=F('CantidadStock') - cantidad)
    
    
    def __str__(self):
        return self.NombreProducto
    
    def entradas_totales(self):
        return sum(entrada.cantidad for entrada in self.entradasuministro_set.all())

    def salidas_totales(self):
        return sum(salida.cantidad for salida in self.salidasuministro_set.all())


class EntradaSuministro(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_entrada = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Entrada de {self.cantidad} unidades de {self.id_producto.NombreProducto} el {self.fecha_entrada}'

    def save(self, *args, **kwargs):
        # Actualizar el campo CantidadStock del modelo Producto
        producto = self.id_producto
        producto.CantidadStock += self.cantidad
        producto.save()

        super().save(*args, **kwargs)
    
class SalidaSuministro(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_salida = models.DateField()
    destino = models.CharField(max_length=255)
    razon = models.TextField()
    numero_autorizacion = models.CharField(max_length=10, blank=True, null=True)  # Número de autorización
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)  # ID del cliente

    def __str__(self):
        return f'Salida de {self.cantidad} unidades de {self.id_producto.nombre} el {self.fecha_salida}'

class AlertaInventario(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_bajo_umbral = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f'Alerta para {self.Producto.NombreProducto} - Bajo Umbral el {self.fecha}'

class MovimientoInventario(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f'{self.tipo_movimiento} de {self.cantidad} unidades de {self.Producto.NombreProducto} el {self.fecha}'
