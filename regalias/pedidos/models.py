from django.db import models

from clientes.models import Cliente

class Pedido(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, models.PROTECT)
    costo = models.FloatField(default=0)
    estado = models.BooleanField(default=False)
    venta = models.BooleanField(default=False)
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
)

class DetallePedido(models.Model):
    material = models.TextField(verbose_name='Material', choices=MATERIALCHOICES)
    descripcion = models.TextField(verbose_name='Descripcion Pedido')
    cantidad = models.IntegerField()
    costo_u = models.FloatField(default=0, verbose_name='Costo Unitario')
    costo_t = models.FloatField(verbose_name='Costo Total')
    pedido = models.ForeignKey(Pedido, models.PROTECT)
    def __unicode__(self):
        return '%s: %s'%(self.pedido.id, self.cantidad)
    def __str__(self):
        return '%s: %s' % (self.pedido.id, self.cantidad)
    class Meta:
        verbose_name = 'Detalle Pedido'
        verbose_name_plural = 'Detalles Pedidos'
        ordering = ['pedido', 'material']