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

CHOICEUNIDAD = (
    ('Kilos', 'Kilos'),
    ('Piezas', 'Piezas'),
)

class Precio(models.Model):
    codigo = models.CharField(max_length=10, verbose_name='Codigo')
    descripcion = models.CharField(max_length=200, verbose_name='Descripcion', help_text='Descripccion del material')
    precio = models.FloatField(verbose_name='Precio Metro L.', help_text='En Bolivianos')
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s: %s Bs. ml'%(self.descripcion, self.precio)
    def __str__(self):
        return '%s: %s Bs. ml' % (self.descripcion, self.precio)
    class Meta:
        verbose_name = 'Tabla de Precio'
        verbose_name_plural = 'Tabla de Precios'
        ordering = ['precio']

COLORCHOICE = (
    ('Azul', 'Azul'),
    ('Rojo', 'Rojo'),
    ('Naranja', 'Naranja'),
    ('Verde', 'Verde'),
)

class MateriaPrima(models.Model):
    nro_serie = models.CharField(max_length=100, verbose_name='Numero de Serie', null=True)
    marca = models.CharField(max_length=100, verbose_name='Marca Producto', null=True)
    cantidad = models.IntegerField(verbose_name='Cantidad', default='1')
    unidad = models.CharField(max_length=50, verbose_name='Unidad', default='Bobina', null=True)
    espesor = models.FloatField(verbose_name='Espesor', help_text='En Milimetros (mm)', null=True)
    ancho = models.FloatField(verbose_name='Ancho', help_text='En Metros Lineales (ml)', null=True)
    superficie = models.CharField(max_length=150, verbose_name='Tratamiento de Superficie', null=True)
    estandar = models.CharField(max_length=150, verbose_name='Estandares', null=True)
    certificacion = models.CharField(max_length=150, verbose_name='Certificaciones', null=True)
    medida = models.CharField(max_length=100, choices=CHOICEUNIDAD, verbose_name='Tipo de Medida', null=True)
    peso = models.IntegerField(verbose_name='Peso', null=True)
    longitud = models.IntegerField(verbose_name='Longitud Aproximada', help_text='En Metros Lineales', null=True)
    color = models.CharField(max_length=100, verbose_name='Color', default='Sin Color', choices=COLORCHOICE)
    fecha = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    estado = models.BooleanField(default=True)
    salida = models.FloatField(default=0, null=True)
    stock = models.FloatField(default=0, null=True)
    proveedor = models.ForeignKey(Proveedor, null=True, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s ml'%self.ancho
    def __str__(self):
        return '%s ml' % self.ancho
    def detalle(self):
        return '%s: %s - %smm * %sml' % (
        self.unidad, self.color, self.espesor, self.ancho)
    class Meta:
        verbose_name = 'Materia Prima Calamina'
        verbose_name_plural = 'Materia Prima Calaminas'
        ordering = ['fecha']