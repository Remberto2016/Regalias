from django import template

register = template.Library()

from django.db.models import Sum

@register.simple_tag
def sum_pedidos(pedidos):
    suma = pedidos.aggregate(Sum('costo_t'))
    if suma['costo_t__sum']:
        return suma['costo_t__sum']
    return 0.0

@register.simple_tag
def total_cantidad(detalles):
    if detalles:
        total = detalles.aggregate(Sum('cantidad'))
        if total['cantidad__sum']:
            return total['cantidad__sum']
        else:
            return 0
    else:
        return 0

@register.simple_tag
def total_metros(detalles):
    if detalles:
        total = detalles.aggregate(Sum('totalm'))
        if total['totalm__sum']:
            return total['totalm__sum']
        else:
            return 0
    else:
        return 0