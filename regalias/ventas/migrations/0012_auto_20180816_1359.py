# Generated by Django 2.0.2 on 2018-08-16 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0011_auto_20180816_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventa',
            name='material',
            field=models.ManyToManyField(to='materiales.MateriaPrima'),
        ),
    ]