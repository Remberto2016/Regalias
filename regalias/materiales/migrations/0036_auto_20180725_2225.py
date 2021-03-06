# Generated by Django 2.0.3 on 2018-07-26 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_empresa_sms'),
        ('materiales', '0035_proveedor_nit'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoCalamina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, verbose_name='Codigo De Calamina')),
            ],
        ),
        migrations.CreateModel(
            name='PrecioCalamina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_codigo', models.CharField(max_length=50)),
                ('precio', models.FloatField(help_text='En Bolivianos', verbose_name='Precio Metro L.')),
                ('espesor', models.FloatField(help_text='En Milimetros (mm)', null=True, verbose_name='Espesor')),
                ('ancho', models.FloatField(help_text='En Metros Lineales (ml)', verbose_name='Ancho')),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Precio de Calamina',
                'verbose_name_plural': 'Precios de Calamina',
                'ordering': ['tipo', 'color', 'codigo'],
            },
        ),
        migrations.CreateModel(
            name='TipoCalamina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50, verbose_name='Tipo De Calamina')),
            ],
        ),
        migrations.AddField(
            model_name='preciocalamina',
            name='codigo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiales.TipoCalamina'),
        ),
        migrations.AddField(
            model_name='preciocalamina',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Color'),
        ),
        migrations.AddField(
            model_name='preciocalamina',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiales.CodigoCalamina'),
        ),
    ]
