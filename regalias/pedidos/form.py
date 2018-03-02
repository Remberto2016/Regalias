#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from pedidos.models import DetallePedido

class DetallePedidoForm(ModelForm):
    class Meta:
        model = DetallePedido
        exclude = ['pedido']