from django import forms
from django.contrib.auth.forms import UserChangeForm

from auth_app.models import ShopUserProfile, ShopUser


class ShopUserEditForm(UserChangeForm):
    """Форма редактирования юзера"""

    username = forms.CharField(
        label='Имя пользователя:',
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
    )

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            self.fields['first_name'].widget.attrs['placeholder'] = 'Иван'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Иванов'
            self.fields['email'].widget.attrs['placeholder'] = 'email@email.ru'
            self.fields['phone'].widget.attrs['placeholder'] = '+79999999999'
            self.fields['phone'].widget.attrs['pattern'] = r'^\+7\d{10,10}$'
            self.fields['phone'].widget.attrs[
                'oninvalid'] = "this.setCustomValidity('Неверный номер " \
                               "телефона! +7999...')"
            self.fields['phone'].widget.attrs[
                'oninput'] = "setCustomValidity('')"


class ProfileEditForm(UserChangeForm):
    """Форма редактирования профиля"""
    gender = forms.ChoiceField(
        label='Пол:',
        choices=(('M', 'Мужчина'), ('W', 'Женщина')),
    )

    class Meta:
        model = ShopUserProfile
        fields = ('about_me', 'gender',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            self.fields['about_me'].widget.attrs[
                'placeholder'] = 'Расскажите о себе...'
