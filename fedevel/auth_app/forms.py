import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
        self.fields['username'].widget.attrs[
            'placeholder'] = 'login, email или номер телефона'
        self.fields['password'].widget.attrs['placeholder'] = 'пароль'


class CompanyUserRegisterForm(UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = ShopUser
        fields = ('first_name', 'last_name', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Иван'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Иванов'
        self.fields['email'].widget.attrs['placeholder'] = 'email@email.ru'
        self.fields['phone'].widget.attrs['placeholder'] = '+79999999999'
        self.fields['phone'].widget.attrs['pattern'] = r'^\+7\d{10,10}$'
        self.fields['phone'].widget.attrs[
            'oninvalid'] = "this.setCustomValidity('Неверный номер " \
                           "телефона! +7999...')"
        self.fields['phone'].widget.attrs['oninput'] = "setCustomValidity('')"
        self.fields['password1'].widget.attrs['placeholder'] = 'пароль'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'повторите пароль'

    def save(self, commit=True):
        user = super().save()
        user.is_active_email = False
        user.is_active_phone = False
        salt = hashlib.sha1(
            str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key_email = hashlib.sha1(
            (user.email + salt).encode('utf8')).hexdigest()
        user.username = salt
        user.save()
        return user
