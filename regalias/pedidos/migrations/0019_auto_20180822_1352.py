# Generated by Django 2.0.2 on 2018-08-22 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0018_auto_20180822_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='usuario',
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
