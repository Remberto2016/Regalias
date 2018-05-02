#encoding:utf-8
from django.forms import ModelForm, TextInput
from django import forms

from pedidos.models import DetallePedido, Pedido
from materiales.models import MateriaPrima, Precio

COLORCHOICE = (
    ('Azul', 'Azul'),
    ('Rojo', 'Rojo'),
    ('Naranja', 'Naranja'),
    ('Verde', 'Verde'),
)

class DetallePedidoForm(ModelForm):
    calamina = forms.ModelChoiceField(label='Tipo Calamina', queryset=Precio.objects.filter(estado=True), required=True)
    largo = forms.FloatField(label='Largo', help_text='En Metros Lineales', min_value=1)
    anchocalamina = forms.ModelChoiceField(label='Ancho', help_text='En Metros Lineales', queryset=MateriaPrima.objects.filter(estado=True))
    color = forms.ChoiceField(label='Color', choices=COLORCHOICE, required=False)
    total_m = forms.FloatField(label='Total Metros', help_text='En Metros Lineales')
    class Meta:
        model = DetallePedido
        fields = ['calamina', 'color', 'anchocalamina', 'unidad', 'largo', 'cantidad', 'total_m', 'costo_u', 'costo_t']
        widgets = {
            'costo_u':TextInput(attrs={'readonly': 'readonly'}),
            'costo_t': TextInput(attrs={'readonly': 'readonly'}),
        }

class ConfirmForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['plazo', 'entrega']