from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    proveedor = models.CharField(max_length=100, verbose_name='Nombre Proveedor')
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s' %self.proveedor
    def __str__(self):
        return '%s' % self.proveedor
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['proveedor']

class MateriaPrima(models.Model):
    nro_serie = models.CharField(max_length=100, verbose_name='Numero de Serie', null=True)
    marca = models.CharField(max_length=100, verbose_name='Marca Producto')
    espesor = models.IntegerField(verbose_name='Espesor', help_text='En Milimetros (mm)')
    ancho = models.IntegerField(verbose_name='Ancho', help_text='En Milimetros (mm)')
    superficie = models.CharField(max_length=150, verbose_name='Tratamiento de Superficie')
    estandar = models.CharField(max_length=150, verbose_name='Estandares')
    certificacion = models.CharField(max_length=150, verbose_name='Certificaciones')
    peso = models.IntegerField(verbose_name='Peso', help_text='En Toneladas (TM)')
    fecha = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    proveedor = models.ForeignKey(Proveedor, null=True, on_delete=models.PROTECT)
    def __unicode__(self):
        return 'Marca: %s - Superficie: %s - Espesor: %s mm - Ancho: %s mm'%(self.marca, self.superficie, self.espesor, self.ancho)
    def __str__(self):
        return 'Marca: %s - Superficie: %s - Espesor: %s mm - Ancho: %s mm' % (self.marca, self.superficie, self.espesor, self.ancho)
    class Meta:
        verbose_name = 'Materia Prima Calamina'
        verbose_name_plural = 'Materia Prima Calaminas'
        ordering = ['fecha']