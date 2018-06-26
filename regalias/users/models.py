# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Empresa(models.Model):
    nit = models.CharField(max_length=300, verbose_name='NIT Empresa')
    nro = models.CharField(max_length=300, verbose_name='Numero de Autorizacion')
    key = models.CharField(max_length=500, verbose_name='Llave de Dosificacion')
    def __unicode__(self):
        return '%s'%self.nit
    def __str__(self):
        return '%s' % self.nit

class Color(models.Model):
    color = models.CharField(max_length=100, verbose_name='Descripcion de Color')
    def __unicode__(self):
        return '%s'%self.color
    def __str__(self):
        return '%s' % self.color
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        ordering = ['color']

class ColorName(models.Model):
    nombre_c = models.CharField(max_length=50)
    hexa = models.CharField(max_length=20)