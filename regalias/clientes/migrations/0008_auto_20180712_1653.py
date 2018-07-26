# Generated by Django 2.0.2 on 2018-07-12 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_auto_20180712_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='ciudad',
            field=models.CharField(max_length=30, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nit',
            field=models.CharField(max_length=20, null=True, unique=True, verbose_name='NIT/CI'),
        ),
        migrations.AlterField(
            model_name='pais',
            name='pais',
            field=models.CharField(max_length=30, unique=True, verbose_name='Nombre'),
        ),
    ]