from django import forms
from django.forms import ModelForm, TextInput

from django.contrib.auth.models import User
from users.models import Empresa, Color, Perfil


from datetime import datetime

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nit', 'nro', 'key', 'sms']

class ColorForm(ModelForm):
    hex = forms.CharField(label='Seleccione Color', widget=TextInput(attrs={'type':'color', 'required':'required'}))
    class Meta:
        model = Color
        fields = ['hex', 'color']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        exclude = ['usuarios']

class EntreFechasSearchForm(forms.Form):
    inicio = forms.DateField(label='Seleccione Fecha de Inicio', widget=forms.TextInput(attrs={'type': 'date', 'required': 'required'}))
    fin = forms.DateField(label='Seleccione Fecha de Finalizacion',
                             widget=forms.TextInput(attrs={'type': 'date', 'required': 'required'}))
    def clean_inicio(self):
        today = datetime.now()
        data = self.cleaned_data['inicio']
        if data.strftime('%Y-%m-%d') > today.strftime('%Y-%m-%d'):
            raise forms.ValidationError('No Puede Seleccionar Una Fecha Mayor a la Actual')
        return data
    def clean_fin(self):
        today = datetime.now()
        data = self.cleaned_data['fin']
        if data.strftime('%Y-%m-%d') > today.strftime('%Y-%m-%d'):
            raise forms.ValidationError('No Puede Seleccionar Una Fecha Mayor a la Actual')
        return data