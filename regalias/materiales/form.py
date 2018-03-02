#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from materiales.models import MateriaPrima, Proveedor

class MateriaPForm(ModelForm):
    class Meta:
        model = MateriaPrima
        exclude = ['user', 'estado']

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['estado']