# Generated by Django 2.0.3 on 2018-03-31 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0006_materiaprima_nro_serie'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiaprima',
            name='longitud',
            field=models.IntegerField(help_text='En Metros Lineales', null=True, verbose_name='Longitud Aproximada'),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='unidad',
            field=models.CharField(choices=[('Kilos', 'Kilos')], max_length=50, null=True, verbose_name='Unidad'),
        ),
        migrations.AlterField(
            model_name='materiaprima',
            name='peso',
            field=models.IntegerField(verbose_name='Peso'),
        ),
    ]
