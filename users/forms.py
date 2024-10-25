from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm


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


class UserRegisterForm(StyleFromMixin, UserCreationForm):
    """ Форма для регистрации нового пользователя."""
   

    class Meta:
        # Поля модели User
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Проверка соответствия паролей
        cd = self.cleaned_data
        validate_password(cd['password1'])
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
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