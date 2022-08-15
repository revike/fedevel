from django.contrib.auth.forms import AuthenticationForm
from django import forms

from auth_app.models import ShopUser


class CompanyUserLoginForm(AuthenticationForm):
    """Форма авторизации"""
    username = forms.CharField(label='')
    password = forms.CharField(label='')

    class Meta:
        model = ShopUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'email или номер телефона'
        self.fields['password'].widget.attrs['placeholder'] = 'пароль'
