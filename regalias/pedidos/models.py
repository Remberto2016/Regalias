from django.db import models

from clientes.models import Cliente
from materiales.models import MateriaPrima

class Pedido(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, models.PROTECT)
    costo = models.FloatField(default=0)
    estado = models.BooleanField(default=False)
    venta = models.BooleanField(default=False)
    entrega = models.CharField(max_length=300, null=True, verbose_name='Lugar de Entrega', help_text='Direccion' )
    plazo = models.IntegerField(default=1, verbose_name='Plazo de Entrega', help_text='En Dias')
    def __unicode__(self):
        return '%s %s'%(self.fecha, self.cliente)
    def __str__(self):
        return '%s %s' % (self.fecha, self.cliente)
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['fecha', 'cliente']

MATERIALCHOICES = (
    ('Calamina', 'Calamina'),
    ('Clavos', 'Clavos'),
)

MATERIALUNIDAD = (
    ('Pieza', 'Pieza'),
    ('Kilos', 'Kilos'),
)

class DetallePedido(models.Model):
    unidad = models.CharField(max_length=50, verbose_name='Unidad de Medida', default='Unidad', choices=MATERIALUNIDAD)
    descripcion = models.TextField(verbose_name='Descripcion Pedido')
    cantidad = models.IntegerField()
    largo = models.FloatField(null=True)
    costo_u = models.FloatField(default=0, verbose_name='Costo Unitario', help_text='En Bolivianos')
    costo_t = models.FloatField(verbose_name='Costo Total', help_text='En Bolivianos')
    pedido = models.ForeignKey(Pedido, models.PROTECT)
    material = models.ManyToManyField(MateriaPrima)
    color = models.CharField(max_length=100, null=True)
    ancho = models.CharField(max_length=10, null=True)
    totalm = models.FloatField(null=True)
    def __unicode__(self):
        return '%s: %s'%(self.pedido.id, self.cantidad)
    def __str__(self):
        return '%s: %s' % (self.pedido.id, self.cantidad)
    class Meta:
        verbose_name = 'Detalle Pedido'
        verbose_name_plural = 'Detalles Pedidos'
        ordering = ['pedido']