# Generated by Django 2.0.3 on 2018-05-16 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_detalleventa_precio_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='largo',
            field=models.FloatField(default=1, null=True),
        ),
    ]
