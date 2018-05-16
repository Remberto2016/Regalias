from django import template

register = template.Library()

from django.db.models import Sum
from ventas.models import DetalleVenta

@register.simple_tag
def salidamaterial(material):
    print(material)
    detalle = DetalleVenta.objects.filter(material='Clavos')
    if detalle:
        sum = detalle.aggregate(Sum('cantidad'))
        return sum['cantidad__sum']
    else:
        return 0