# En forms.py

from django import forms
from .models import EntradaSuministro
from .models import Producto, Proveedor
from .models import Cliente
from .models import EntidadSalud
# forms.py
from .models import SalidaSuministro
# En forms.py
# En forms.py

from django import forms
from .models import Proveedor


class EntidadSaludForm(forms.ModelForm):
    class Meta:
        model = EntidadSalud
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


class SalidaSuministroForm(forms.ModelForm):
    class Meta:
        model = SalidaSuministro
        fields = ['id_producto', 'cantidad', 'fecha_salida', 'destino', 'razon', 'numero_autorizacion', 'id_cliente']

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        id_producto = cleaned_data.get('id_producto')

        if cantidad is not None and id_producto is not None:
            # Validar que la cantidad no sea mayor que el stock disponible
            if cantidad > id_producto.CantidadStock:
                raise forms.ValidationError('La cantidad de salida es mayor que el stock disponible.')

        return cleaned_data
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'nombre', 'direccion', 'telefono', 'tipo_cliente', 'entidad_salud']

class EntradaSuministroForm(forms.ModelForm):
    class Meta:
        model = EntradaSuministro
        fields = ['id_producto', 'cantidad', 'fecha_entrada', 'proveedor']

    

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar el campo de categoría como una lista desplegable
        self.fields['categoria'].widget = forms.Select(choices=Producto.CATEGORIAS)
        # Configurar el campo de proveedor para mostrar el nombre en lugar del ID
        self.fields['Proveedor'].queryset = Proveedor.objects.all()

    def save(self, *args, **kwargs):
        # Generar el ID personalizado aquí, por ejemplo, "P0000001"
        if not self.instance.pk:
            # Solo generar un nuevo ID si el producto no tiene una clave primaria (es nuevo)
            ultimo_producto = Producto.objects.order_by('-id').first()
            nuevo_id = 'P0000001'  # Esto podría ser más complejo según tus necesidades
            if ultimo_producto and ultimo_producto.id:
                ultimo_id = int(ultimo_producto.id[1:])
                nuevo_id = f'P{str(ultimo_id + 1).zfill(7)}'
            self.instance.id = nuevo_id
        super().save(*args, **kwargs)

    def clean_id(self):
        # Validar el ID aquí si es necesario
        id = self.cleaned_data['id']
        # Tu lógica de validación personalizada
        # ...
        return id
