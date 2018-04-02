from __future__ import unicode_literals
from django.db import models

from django.core.exceptions import ValidationError

def validate_ci(value):
    if len(str(value)) != 10 and len(str(value)) != 8 and len(str(value)) != 7:
        raise ValidationError(u'%s No es un Cedula de Identidad'% value)
    return validate_ci

GENERO = (
    ('Masculino','Masculino'),
    ('Femenino', 'Femenino'),
)

class Pais(models.Model):
    pais = models.CharField(max_length=30, verbose_name='País')
    def __str__(self):
        return self.pais
    def __unicode__(self):
        return self.pais
    class Meta:
        ordering = ['pais']
        verbose_name = 'País'
        verbose_name_plural = 'Paices'

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=30, verbose_name='Ciudad')
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    def __str__(self):
        return self.ciudad
    def __unicode__(self):
        return self.ciudad
    class Meta:
        ordering = ['pais', 'ciudad']
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Cliente(models.Model):
    ci = models.CharField(validators=[validate_ci], max_length=10,unique=True, verbose_name='Cedula de Identidad')
    nit = models.CharField(max_length=20, verbose_name='NIT', null=True)
    nombres = models.CharField(max_length=50, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    direccion = models.CharField(max_length=50, verbose_name='Direccion')
    telefono = models.CharField(max_length=15, verbose_name='Telefono/Ceular')
    email = models.EmailField(blank=True, verbose_name='Correo Electronico')
    ciudad = models.ForeignKey(Ciudad, verbose_name='Ciudad', on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s %s' % (self.nombres, self.apellidos)
    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)