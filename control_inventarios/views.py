# En views.py

from http.client import HTTPResponse
from django.shortcuts import render, redirect

from .forms import EntradaSuministroForm
from .models import EntradaSuministro, Producto, SalidaSuministro  # Agregado desde 24092023
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.shortcuts import render, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from .models import EntidadSalud
from .forms import EntidadSaludForm
from .forms import SalidaSuministroForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm
from .models import Proveedor
from django.http import HttpResponse, JsonResponse
from .resources import EntradaSuministroResource, SalidaSuministroResource
from tablib import Dataset
from .models import EntradaSuministro, SalidaSuministro
from django.shortcuts import render, redirect

# from django.contrib.auth import logout

from django.shortcuts import redirect


def exportar_entradas(request):
    # Lógica de filtrado para exportar solo los datos deseados
    # Puedes obtener los parámetros de filtro desde la URL o utilizar un formulario de filtrado

    # Ejemplo: Filtrar por producto, fecha, etc.
    producto_id = request.GET.get('producto_id')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    queryset = EntradaSuministro.objects.all()

    if producto_id:
        queryset = queryset.filter(id_producto=producto_id)

    # Agregar más lógica de filtro según tus necesidades

    dataset = EntradaSuministroResource().export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=entradas_suministros.xlsx'
    return response

def exportar_salidas(request):
    # Lógica de filtrado similar a exportar_entradas
    # ...

    dataset = SalidaSuministroResource().export(queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=salidas_suministros.xlsx'
    return response

def consultar_entradas(request):
    # Lógica para obtener datos de la consulta (puedes usar request.GET)
    # Ejemplo: 
    producto_id = request.GET.get('producto_id')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    proveedor_id = request.GET.get('proveedor_id')

    # Lógica para filtrar las entradas según los parámetros de la consulta
    entradas = EntradaSuministro.objects.all()

    if producto_id:
        entradas = entradas.filter(id_producto=producto_id)
    if fecha_inicio:
        entradas = entradas.filter(fecha_entrada__gte=fecha_inicio)
    if fecha_fin:
        entradas = entradas.filter(fecha_entrada__lte=fecha_fin)
    if proveedor_id:
        entradas = entradas.filter(proveedor_id=proveedor_id)

    # Lógica para renderizar la plantilla con los resultados
    return render(request, 'consultar_entradas.html', {'entradas': entradas})

def consultar_salidas(request):
    # Lógica para obtener datos de la consulta (puedes usar request.GET)
    # Ejemplo:
    cliente_id = request.GET.get('cliente_id')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    destino = request.GET.get('destino')

    # Lógica para filtrar las salidas según los parámetros de la consulta
    salidas = SalidaSuministro.objects.all()

    if cliente_id:
        salidas = salidas.filter(id_cliente=cliente_id)
    if fecha_inicio:
        salidas = salidas.filter(fecha_salida__gte=fecha_inicio)
    if fecha_fin:
        salidas = salidas.filter(fecha_salida__lte=fecha_fin)
    if destino:
        salidas = salidas.filter(destino=destino)

    # Lógica para renderizar la plantilla con los resultados
    return render(request, 'consultar_salidas.html', {'salidas': salidas})




# Vista para listar todos los proveedores


def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'control_inventarios/listar_proveedores.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'control_inventarios/crear_proveedor.html', {'form': form})

def editar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'control_inventarios/editar_proveedor.html', {'form': form, 'id_proveedor': id_proveedor})

def borrar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('listar_proveedores')
    return render(request, 'control_inventarios/borrar_proveedor.html', {'proveedor': proveedor})

def inventario_data(request):
    inventario = Producto.objects.all()
    data = []

    for producto in inventario:
        data.append({
            'Producto': producto.NombreProducto,
            'CantidadStock': producto.CantidadStock,
            'EntradasTotales': producto.entradas_totales(),
            'SalidasTotales': producto.salidas_totales(),
        })

    return JsonResponse(data, safe=False)


from django.db.models import F

# ... Otras importaciones ...

def registrar_salida(request):
    if request.method == 'POST':
        form = SalidaSuministroForm(request.POST)
        if form.is_valid():
            salida = form.save()

            # Actualizar el stock después de registrar la salida
            producto = salida.id_producto
            cantidad_salida = salida.cantidad
            producto.CantidadStock -= cantidad_salida
            producto.save()

           

            return redirect('salida_exitosa')
    else:
        form = SalidaSuministroForm()

    return render(request, 'registrar_salida.html', {'form': form})




def salida_exitosa(request):
    return render(request, 'salida_exitosa.html')  # Puedes ajustar el nombre del archivo de plantilla según tu estructura

def index(request):
    return render(request, 'index.html')


def registrar_entrada(request):
    if request.method == 'POST':
        form = EntradaSuministroForm(request.POST)
        if form.is_valid():
            entrada = form.save()
            return redirect('entrada_exitosa')  # Puedes crear una vista para mostrar un mensaje de entrada exitosa
    else:
        form = EntradaSuministroForm()
    
    return render(request, 'registrar_entrada.html', {'form': form})

def entrada_exitosa(request):
    return render(request, 'entrada_exitosa.html')

#Agregamos desde 24092023
def visualizar_inventario(request):
    # Obtén los datos del inventario, por ejemplo, todos los productos
    inventario = Producto.objects.all()

    # Pasa los datos a la plantilla
    return render(request, 'inventario.html', {'inventario': inventario})

@login_required
def visualizar_inventario(request):
    # Verificar que el usuario sea un gerente o un administrador
    

    # Obtener los datos del inventario
    inventario = Producto.objects.all()

    # Pasa los datos a la plantilla
    return render(request, 'inventario.html', {'inventario': inventario})

# Productos
def productos(request):
    return render(request, 'producto/productos.html')

def listar_productos(request):
    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()

    # Puedes agregar más lógica según tus necesidades, como filtrar, ordenar, etc.

    return render(request, 'control_inventarios/listar_productos.html', {'productos': productos})

def crear_producto(request):
    productos = Producto.objects.all()
    form = ProductoForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('crear_producto')

    return render(request, 'control_inventarios/crear_producto.html', {'productos': productos, 'form': form})


def editar_producto(request, pk):
    # Asegúrate de que pk sea un valor válido y se pueda convertir a un entero
    try:
        pk = str(pk)
    except ValueError:
        # Manejo de error si pk no es un número válido
        return HTTPResponse("ID de producto no válido")

    # Obtiene el objeto Producto con el pk proporcionado o muestra un error 404 si no existe
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'control_inventarios/editar_producto.html', {'form': form, 'pk': pk, 'producto': producto})



def eliminar_producto(request):
    if request.method == 'POST':
        productos_seleccionados = request.POST.getlist('productos_seleccionados')
        Producto.objects.filter(id__in=productos_seleccionados).delete()
    
    return redirect('listar_productos')

# Clientes


# Vista para listar todos los clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'control_inventarios/listar_clientes.html', {'clientes': clientes})

# Vista para crear un nuevo cliente
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'control_inventarios/crear_cliente.html', {'form': form})

# Vista para editar un cliente existente
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'control_inventarios/editar_cliente.html', {'form': form})

# Vista para borrar un cliente existente
def borrar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'control_inventarios/borrar_cliente.html', {'cliente': cliente})

def clientes(request):
    # Recupera la lista de clientes desde tu base de datos o donde estén almacenados
    clientes = Cliente.objects.all()  # Otra consulta según tu modelo

    # Asegúrate de que cada cliente tenga un 'id_cliente' válido
    for cliente in clientes:
        if not cliente.id_cliente:
            # Puedes asignar un valor predeterminado o manejarlo de otra manera
            cliente.id_cliente = 'ValorPredeterminado'

    return render(request, 'clientes/clientes.html', {'clientes': clientes})

def proveedor(request):
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
    for proveedor in proveedores:
        if not Proveedor.id_proveedor:
            # Puedes asignar un valor predeterminado o manejarlo de otra manera
            Proveedor.id_proveedor = 'ValorPredeterminado'

    return render(request, 'proveedor/proveedores.html', {'proveedores': proveedores})


# Entidades de Salud
def entidades(request):
    entidades_salud = EntidadSalud.objects.all()

    # Iterar sobre las instancias de EntidadSalud
    for entidad in entidades_salud:
        if not entidad.id_entidad:
            # Puedes asignar un valor predeterminado o manejarlo de otra manera
            entidad.id_entidad = 'ValorPredeterminado'

    return render(request, 'entidadsalud/entidades.html', {'entidades': entidades_salud})

def lista_entidades_salud(request):
    entidades_salud = EntidadSalud.objects.all()
    return render(request, 'lista_entidades_salud.html', {'entidades_salud': entidades_salud})

def detalle_entidad_salud(request, id_entidad):
    entidad_salud = get_object_or_404(EntidadSalud, id_entidad=id_entidad)
    return render(request, 'detalle_entidad_salud.html', {'entidad_salud': entidad_salud})

def editar_entidad_salud(request, id_entidad):
    entidad_salud = get_object_or_404(EntidadSalud, id_entidad=id_entidad)

    if request.method == 'POST':
        form = EntidadSaludForm(request.POST, instance=entidad_salud)
        if form.is_valid():
            form.save()
            # Puedes redirigir a una página de detalle o a la lista de entidades de salud
            return redirect('detalle_entidad_salud', id_entidad=id_entidad)

    else:
        form = EntidadSaludForm(instance=entidad_salud)

    return render(request, 'editar_entidad_salud.html', {'form': form, 'entidad_salud': entidad_salud})

def borrar_entidad_salud(request, id_entidad):
    entidad_salud = get_object_or_404(EntidadSalud, id_entidad=id_entidad)
    if request.method == 'POST':
        entidad_salud.delete()
        return redirect('lista_entidades_salud')
    return render(request, 'borrar_entidad_salud.html', {'entidad_salud': entidad_salud})

def crear_entidad_salud(request):
    if request.method == 'POST':
        form = EntidadSaludForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_entidades_salud')
    else:
        form = EntidadSaludForm()

    return render(request, 'crear_entidad_salud.html', {'form': form})

