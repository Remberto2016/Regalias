# Generated by Django 2.0.3 on 2018-08-14 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0039_auto_20180813_2128'),
        ('pedidos', '0013_auto_20180627_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='preciocalamina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='materiales.PrecioCalamina'),
        ),
    ]