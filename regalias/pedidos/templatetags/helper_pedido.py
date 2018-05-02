from django import template

register = template.Library()

from django.db.models import Sum

@register.simple_tag
def sum_pedidos(pedidos):
    suma = pedidos.aggregate(Sum('costo_t'))
    if suma['costo_t__sum']:
        return suma['costo_t__sum']
    return 0.0