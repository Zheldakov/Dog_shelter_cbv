from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm


class StyleFromMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFromMixin, forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone',)


class UserRegisterForm(StyleFromMixin, forms.ModelForm):
    """ Форма для регистрации нового пользователя."""
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=8, max_length=12) # c спроверкой поля
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput) # тут свой валидатор
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        # Поля модели User
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Проверка соответствия паролей
        cd = self.cleaned_data
        print(cd)
        validate_password(cd['password'])
        if cd['password'] != cd['password2']:
            print('Пароли не совпадают')
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserLoginForm(StyleFromMixin, forms.Form):
    """ Форма для авторизации пользователя."""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(StyleFromMixin, forms.ModelForm):
    """ Форма для изменения пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'telegram', 'avatar',)

class UserPasswordChangeForm(StyleFromMixin, PasswordChangeForm):
    """ Форма для смены пароля."""
    pass