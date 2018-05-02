# Generated by Django 2.0.3 on 2018-04-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_cliente_razon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='apellidos',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='ci',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nombres',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nit',
            field=models.CharField(max_length=20, null=True, verbose_name='NIT/CI'),
        ),
    ]
