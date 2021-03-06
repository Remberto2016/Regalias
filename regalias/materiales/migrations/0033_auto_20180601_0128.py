# Generated by Django 2.0.3 on 2018-06-01 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0032_auto_20180516_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePrecioClavo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('precioclavo', models.ForeignKey(on_delete=models.Model, to='materiales.PrecioClavos')),
            ],
        ),
        migrations.AlterField(
            model_name='precio',
            name='color',
            field=models.CharField(default='Sin Color', max_length=100, null=True, verbose_name='Color'),
        ),
    ]
