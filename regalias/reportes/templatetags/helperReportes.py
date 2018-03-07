from django import template

register = template.Library()

from django.db.models import Sum

@register.simple_tag
def count_ventas(ventas, month):
    vent = ventas.filter(fecha__month = month)
    if(vent):
        return vent.count()
    else:
        return 0

@register.simple_tag
def count_pedidos(pedidos, month):
    vent = pedidos.filter(fecha__month = month)
    if(vent):
        return vent.count()
    else:
        return 0