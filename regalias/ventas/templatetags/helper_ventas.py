from django import template

register = template.Library()

from django.db.models import Sum

@register.simple_tag
def sum_ventas(ventas):
    suma = ventas.aggregate(Sum('costo'))
    if suma['costo__sum']:
        return suma['costo__sum']
    return 0.0
    
@register.simple_tag
def sum_ventas_t(ventas):
    suma = ventas.aggregate(Sum('costo_t'))
    if suma['costo_t__sum']:
        return suma['costo_t__sum']
    return 0.0