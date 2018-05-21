from django.db import models
from django.contrib.auth.models import User

from clientes.models import Ciudad

class Proveedor(models.Model):
    proveedor = models.CharField(max_length=100, verbose_name='Nombre Proveedor')
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    estado = models.BooleanField(default=True)
    origen = models.ForeignKey(Ciudad, null=True, on_delete=models.PROTECT, verbose_name='Ciudad de origen')
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
)

COLORCHOICE = (
    ('Azul', 'Azul'),
    ('Rojo', 'Rojo'),
    ('Naranja', 'Naranja'),
    ('Verde', 'Verde'),
)

TIPOCHOICES = (
    ('Calamina', 'Calamina'),
    ('Clavos', 'Clavos'),
)

UNIDADCHOICES = (
    ('Bobina', 'Bobina'),
    ('Alambron', 'Alambron'),
)

class MateriaPrima(models.Model):
    tipo = models.CharField(max_length=10, verbose_name='Tipo Material', default='Calamina', choices=TIPOCHOICES)
    nro_serie = models.CharField(max_length=100, verbose_name='Numero de Serie', null=True)
    marca = models.CharField(max_length=100, verbose_name='Marca Producto')
    cantidad = models.IntegerField(verbose_name='Cantidad', default='1')
    unidad = models.CharField(max_length=50, verbose_name='Unidad', default='Bobina', null=True, choices=UNIDADCHOICES)
    espesor = models.FloatField(verbose_name='Espesor', help_text='En Milimetros (mm)')
    ancho = models.FloatField(verbose_name='Ancho', help_text='En Metros Lineales (ml)', null=True, blank=True, default=0)
    medida = models.CharField(max_length=100, choices=CHOICEUNIDAD, verbose_name='Tipo de Medida', null=True)
    peso = models.IntegerField(verbose_name='Peso')
    longitud = models.IntegerField(verbose_name='Longitud Aproximada', help_text='En Metros Lineales', null=True, blank=True, default=0)
    color = models.CharField(max_length=100, verbose_name='Color', default='Sin Color', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    salida = models.FloatField(default=0)
    precioc = models.FloatField(default=0, verbose_name='Precio de Compra', help_text='En Bolivianos')
    stock = models.FloatField(default=0)
    proveedor = models.ForeignKey(Proveedor, null=True, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s: %s de   %smm de espesor * %sml de ancho' % (
            self.unidad, self.color, self.espesor, self.ancho)
    def __str__(self):
        return '%s: %s de   %smm de espesor * %sml de ancho' % (
            self.unidad, self.color, self.espesor, self.ancho)
    def detalle(self):
        return '%s: %s de   %smm de espesor * %sml de ancho' % (
        self.unidad, self.color, self.espesor, self.ancho)
    class Meta:
        verbose_name = 'Materia Prima Calamina'
        verbose_name_plural = 'Materia Prima Calaminas'
        ordering = ['fecha']

class Precio(models.Model):
    codigo = models.CharField(max_length=10, verbose_name='Codigo')
    materia = models.ForeignKey(MateriaPrima, null=True, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=200, verbose_name='Descripcion')
    precio = models.FloatField(verbose_name='Precio Metro L.', help_text='En Bolivianos')
    espesor = models.FloatField(verbose_name='Espesor', help_text='En Milimetros (mm)', null=True)
    color = models.CharField(max_length=100, verbose_name='Color', default='Sin Color', null=True)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s: %s Bs. ml'%(self.descripcion, self.precio)
    def __str__(self):
        return '%s: %s Bs. ml' % (self.descripcion, self.precio)
    class Meta:
        verbose_name = 'Tabla de Precio'
        verbose_name_plural = 'Tabla de Precios'
        ordering = ['precio']


TIPESCLAVOS = (
    ('Unidad', 'Unidad'),
    ('Caja', 'Caja'),
)

class PrecioClavos(models.Model):
    codigo = models.CharField(max_length=10, verbose_name='Codigo')
    tipo = models.CharField(max_length=20, null=True, choices=TIPESCLAVOS)
    descripcion = models.CharField(max_length=200, verbose_name='Descripcion')
    precio = models.FloatField(verbose_name='Precio Kilo.', help_text='En Bolivianos')
    longitud = models.FloatField(verbose_name='Longitud', help_text='En Milimetros (mm)', null=True)
    stock = models.IntegerField(default=1, help_text='En Kilos')
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s: %s Bs. ml'%(self.descripcion, self.precio)
    def __str__(self):
        return '%s: %s Bs. ml' % (self.descripcion, self.precio)
    class Meta:
        verbose_name = 'Tabla de Precio Clavo'
        verbose_name_plural = 'Tabla de Precios Clavos'
        ordering = ['precio']