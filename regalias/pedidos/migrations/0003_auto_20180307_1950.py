# Generated by Django 2.0.2 on 2018-03-07 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedido_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='unidad',
            field=models.CharField(choices=[('Unidad', 'Unidad'), ('Kilos', 'Kilos')], default='Unidad', max_length=50, verbose_name='Unidad de Medida'),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='material',
            field=models.TextField(choices=[('Calamina', 'Calamina'), ('Clavos', 'Clavos')], verbose_name='Material'),
        ),
    ]
