# Generated by Django 2.0.3 on 2018-05-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0026_precioclavos'),
    ]

    operations = [
        migrations.AddField(
            model_name='precioclavos',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]