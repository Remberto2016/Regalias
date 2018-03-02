from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']