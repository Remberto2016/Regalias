from django import forms
from django.forms import ModelForm, TextInput

from django.contrib.auth.models import User
from users.models import Empresa, Color, Perfil

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nit', 'nro', 'key', 'sms', 'vencimiento']
        widgets= {
        'vencimiento':TextInput(attrs={'readonly': 'readonly'}),
        }

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