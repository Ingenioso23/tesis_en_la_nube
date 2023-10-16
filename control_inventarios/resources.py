# En tu_app/resources.py
from import_export import resources
from .models import EntradaSuministro, SalidaSuministro

class EntradaSuministroResource(resources.ModelResource):
    class Meta:
        model = EntradaSuministro

class SalidaSuministroResource(resources.ModelResource):
    class Meta:
        model = SalidaSuministro
