# Generated by Django 2.0.3 on 2018-04-02 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0014_auto_20180401_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiaprima',
            name='color',
            field=models.CharField(choices=[('Azul', 'Azul'), ('Rojo', 'Rojo'), ('Naranja', 'Naranja'), ('Verde', 'Verde')], default='Sin Color', max_length=100, verbose_name='Color'),
        ),
    ]
