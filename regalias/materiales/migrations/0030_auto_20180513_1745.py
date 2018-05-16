# Generated by Django 2.0.3 on 2018-05-13 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0029_precioclavos_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='precio',
            name='materia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='materiales.MateriaPrima'),
        ),
        migrations.AlterField(
            model_name='precioclavos',
            name='tipo',
            field=models.CharField(choices=[('Unidad', 'Unidad'), ('Caja', 'Caja')], max_length=20, null=True),
        ),
    ]
