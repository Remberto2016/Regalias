# Generated by Django 2.0.3 on 2018-04-15 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0018_auto_20180415_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiaprima',
            name='espesor',
            field=models.FloatField(help_text='En Milimetros (mm)', verbose_name='Espesor'),
        ),
        migrations.AlterField(
            model_name='precio',
            name='espesor',
            field=models.FloatField(help_text='En Milimetros (mm)', null=True, verbose_name='Espesor'),
        ),
    ]
