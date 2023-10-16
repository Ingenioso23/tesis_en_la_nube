# Generated by Django 4.2.6 on 2023-10-15 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('tipo_cliente', models.CharField(choices=[('Interno', 'Interno'), ('Externo', 'Externo')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EntidadSalud',
            fields=[
                ('id_entidad', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('categoria', models.CharField(choices=[('Medicamento', 'Medicamento'), ('Suministro', 'Suministro')], max_length=255)),
                ('TipoProducto', models.CharField(max_length=255)),
                ('NombreProducto', models.CharField(max_length=255)),
                ('NumeroLote', models.CharField(max_length=255)),
                ('FechaVencimiento', models.DateField(default=None)),
                ('CantidadStock', models.IntegerField(default=0)),
                ('Concentracion', models.CharField(max_length=255)),
                ('FormaFarmaceutica', models.CharField(max_length=255)),
                ('NumeroReferencia', models.CharField(max_length=255)),
                ('UnidadesMedida', models.CharField(max_length=255)),
                ('UbicacionAlmacen', models.CharField(max_length=255)),
                ('NivelReorden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SalidaSuministro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha_salida', models.DateField()),
                ('destino', models.CharField(max_length=255)),
                ('razon', models.TextField()),
                ('numero_autorizacion', models.CharField(blank=True, max_length=10, null=True)),
                ('id_cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control_inventarios.cliente')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.producto')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='Proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.proveedor'),
        ),
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_movimiento', models.CharField(max_length=255)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.producto')),
            ],
        ),
        migrations.CreateModel(
            name='EntradaSuministro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha_entrada', models.DateField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.proveedor')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='entidad_salud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control_inventarios.entidadsalud'),
        ),
        migrations.CreateModel(
            name='AlertaInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_bajo_umbral', models.IntegerField()),
                ('fecha', models.DateField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_inventarios.producto')),
            ],
        ),
    ]