from django import template

register = template.Library()

from django.db.models import Sum

@register.simple_tag
def sum_ventas(ventas):
    suma = ventas.aggregate(Sum('costo_t'))
    if suma['costo__sum']:
        return suma['costo__sum']
    return 0.0