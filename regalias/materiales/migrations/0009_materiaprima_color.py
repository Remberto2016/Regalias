# Generated by Django 2.0.3 on 2018-03-31 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0008_auto_20180331_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiaprima',
            name='color',
            field=models.CharField(default='Sin Color', max_length=100, verbose_name='Color'),
        ),
    ]
