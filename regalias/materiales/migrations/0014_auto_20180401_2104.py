# Generated by Django 2.0.3 on 2018-04-02 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0013_auto_20180401_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiaprima',
            name='salida',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='stock',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='materiaprima',
            name='ancho',
            field=models.FloatField(help_text='En Metros Lineales (ml)', verbose_name='Ancho'),
        ),
    ]
