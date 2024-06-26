from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')
