# Generated by Django 2.0.2 on 2018-02-20 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0002_materiaprima_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proveedor', models.CharField(max_length=100, verbose_name='Nombre Proveedor')),
                ('telefono', models.CharField(max_length=10)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['proveedor'],
            },
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='materiales.Proveedor'),
        ),
    ]
