from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from users.models import Empresa, Color

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = '__all__'