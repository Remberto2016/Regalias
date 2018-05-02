#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from users.models import Color
from clientes.models import Pais
from materiales.models import MateriaPrima, Proveedor, Precio, PrecioClavos

import datetime
class MateriaPForm(ModelForm):
    colores = forms.ModelChoiceField(label='Color', queryset=Color.objects.all(), required=False)
    class Meta:
        model = MateriaPrima
        exclude = ['user', 'estado', 'salida', 'stock', 'cantidad', 'color']

class ProveedorForm(ModelForm):
    pais = forms.ModelChoiceField(label='Pais', queryset=Pais.objects.all())
    class Meta:
        model = Proveedor
        fields = ['proveedor', 'telefono', 'pais', 'origen', 'direccion', 'email']

class PrecioForm(ModelForm):
    class Meta:
        model = Precio
        exclude = ['estado']

class SearchProveedor(forms.Form):
    proveedor = forms.ModelChoiceField(label='Seleccione Proveedor',
                                       queryset=Proveedor.objects.filter(estado=True), required=True)
    hoy = datetime.datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = int(anho) - 10
    a_fin = int(anho) + 1
    anhos = ()
    for a in range(a_ini, a_fin):
        anhos += ((a, a),)
    year = forms.ChoiceField(choices=anhos, label=u'Seleccione Año')
    meses = (
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    )
    month = forms.ChoiceField(choices=meses, label="Seleccione un Mes")

class PrecioClavoForm(ModelForm):
    class Meta:
        model = PrecioClavos
        exclude = ['estado']