# Generated by Django 2.0.2 on 2018-02-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0005_proveedor_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiaprima',
            name='nro_serie',
            field=models.CharField(max_length=100, null=True, verbose_name='Numero de Serie'),
        ),
    ]
