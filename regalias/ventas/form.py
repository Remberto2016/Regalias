#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from materiales.models import MateriaPrima
from ventas.models import DetalleVenta

CHOICE_LARGE = (
    ('', '---------'),
    ('500', '500'),
    ('1000', '1000'),
    ('1500', '1500'),
    ('2000', '2000'),
    ('2500', '2500'),
    ('3000', '3000'),
    ('3500', '3500'),
    ('4000', '4000'),
    ('4500', '4500'),
    ('5000', '5000'),
)

class DetalleVentaForm(ModelForm):
    materiaprima = forms.ModelChoiceField(label='Seleccione Materia Prima',
                                          queryset=MateriaPrima.objects.filter(estado=True), required=True)
    largo = forms.ChoiceField(label='Seleccione Largo', help_text='En Milimetros', choices=CHOICE_LARGE)
    class Meta:
        model = DetalleVenta
        fields = ['materiaprima', 'largo', 'material', 'descripcion', 'cantidad', 'costo_u', 'costo_t']