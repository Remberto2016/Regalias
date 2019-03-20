#encoding:utf-8
from django.forms import ModelForm, TextInput, Textarea
from django import forms


from materiales.models import MateriaPrima, PrecioClavos
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
    materiaprima = forms.ModelChoiceField(label='Seleccione Clavo',
                                          queryset=PrecioClavos.objects.filter(estado=True), required=True)
    class Meta:
        model = DetalleVenta
        fields = ['materiaprima', 'unidad', 'descripcion', 'cantidad', 'costo_u', 'costo_t']
        exclude = ['material']
        widgets = {
        'costo_u':TextInput(attrs={'readonly': 'readonly'}),
        'costo_t':TextInput(attrs={'readonly': 'readonly'}),
        'descripcion':Textarea(attrs={'rows':3}),
        }