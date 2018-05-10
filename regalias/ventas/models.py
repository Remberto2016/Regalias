from django.db import models

from clientes.models import Cliente

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, models.PROTECT)
    costo = models.FloatField(default=0)
    estado = models.BooleanField(default=False)
    nro_venta = models.IntegerField(null=True)
    def __unicode__(self):
        return '%s %s'%(self.fecha, self.cliente)
    def __str__(self):
        return '%s %s' % (self.fecha, self.cliente)
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['fecha', 'cliente']

MATERIALCHOICES = (
    ('Calamina', 'Calamina'),
    ('Clavos', 'Clavos'),
)

MATERIALUNIDAD = (
    ('Unidad', 'Unidad'),
    ('Kilos', 'Kilos'),
)

class DetalleVenta(models.Model):
    material = models.TextField(verbose_name='Material', choices=MATERIALCHOICES)
    unidad = models.CharField(max_length=50, verbose_name='Unidad de Medida', default='Unidad', choices=MATERIALUNIDAD)
    descripcion = models.TextField(verbose_name='Descripcion Pedido')
    cantidad = models.IntegerField()
    costo_u = models.FloatField(default=0, verbose_name='Costo Unitario')
    costo_t = models.FloatField(verbose_name='Costo Total')
    venta = models.ForeignKey(Venta, models.PROTECT)
    precio_id = models.IntegerField(null=True)
    def __unicode__(self):
        return '%s: %s'%(self.venta.id, self.cantidad)
    def __str__(self):
        return '%s: %s' % (self.venta.id, self.cantidad)
    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ['venta', 'material']