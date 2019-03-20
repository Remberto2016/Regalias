from django.db import models
from django.contrib.auth.models import User

from clientes.models import Cliente
from materiales.models import PrecioCalamina, PrecioClavos

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, models.PROTECT)
    costo = models.FloatField(default=0)
    estado = models.BooleanField(default=False)
    nro_venta = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
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
    ('Kilos', 'Kilos'),
    ('Calamina', 'Calamina'),
)

from materiales.models import MateriaPrima

class DetalleVenta(models.Model):
    preciocalamina = models.ForeignKey(PrecioCalamina, models.PROTECT, null=True)
    precioclavos = models.ForeignKey(PrecioClavos, models.PROTECT, null=True)
    material = models.ManyToManyField(MateriaPrima)
    unidad = models.CharField(max_length=50, verbose_name='Unidad de Medida', default='Kilos', choices=MATERIALUNIDAD)
    descripcion = models.TextField(verbose_name='Descripción')
    cantidad = models.IntegerField()
    costo_u = models.FloatField(default=0, verbose_name='Costo Unitario')
    costo_t = models.FloatField(verbose_name='Costo Total')
    venta = models.ForeignKey(Venta, models.PROTECT)
    largo = models.FloatField(default=1, null=True)
    precio_id = models.IntegerField(null=True)
    tipo = models.CharField(max_length=50, null=True)
    totalm = models.FloatField(null=True) 
   
    #materia_id = models.ForeignKey(MateriaPrima, null=True, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s: %s'%(self.venta.id, self.cantidad)
    def __str__(self):
        return '%s: %s' % (self.venta.id, self.cantidad)
    def information(self):
        if self.preciocalamina:
            return '%s  %s mm.  x %s mm.' % (self.preciocalamina.tipo, self.preciocalamina.espesor, self.preciocalamina.ancho)
        else:
            return '%s' % (self.unidad)
    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ['venta', 'preciocalamina']