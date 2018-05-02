#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from clientes.models import Pais, Ciudad, Cliente

class PaisForm(ModelForm):
    class Meta:
        model = Pais
        fields = '__all__'

class CiudadForm(ModelForm):
    class Meta:
        model = Ciudad
        fields = '__all__'

class ClienteForm(ModelForm):
    pais = forms.ModelChoiceField(label='Seleccione Pais', queryset=Pais.objects.all(), required=True)
    class Meta:
        model = Cliente
        fields = ['nit', 'razon', 'pais', 'ciudad', 'direccion', 'telefono', 'email']