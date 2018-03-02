#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from ventas.models import DetalleVenta

class DetalleVentaForm(ModelForm):
    class Meta:
        model = DetalleVenta
        exclude = ['venta']