from django import template

register = template.Library()

from django.db.models import Sum
from ventas.models import DetalleVenta

@register.simple_tag
def salidamaterial(material):
    print(material)
    detalle = DetalleVenta.objects.filter(material='Clavos', precio_id=material.id)
    if detalle:
        sum = detalle.aggregate(Sum('cantidad'))
        return sum['cantidad__sum']
    else:
        return 0

@register.simple_tag
def sumita(largo, cantidad):
    return float(largo) * float(cantidad)