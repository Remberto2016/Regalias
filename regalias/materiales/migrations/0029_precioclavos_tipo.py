# Generated by Django 2.0.3 on 2018-05-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0028_auto_20180506_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='precioclavos',
            name='tipo',
            field=models.CharField(choices=[('Calamina', 'Calamina'), ('Clavos', 'Clavos')], max_length=20, null=True),
        ),
    ]