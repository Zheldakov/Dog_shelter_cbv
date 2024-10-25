from django import forms


from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

from users.models import User
from users.validators import validate_password

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
            raise forms.ValidationError('password_mismatch')
        return cd['password2']


class UserLoginForm(StyleFromMixin, AuthenticationForm):
    """ Форма для авторизации пользователя."""
    pass


class UserUpdateForm(StyleFromMixin, forms.ModelForm):
    """ Форма для изменения пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'telegram', 'avatar',)


class UserPasswordChangeForm(StyleFromMixin, PasswordChangeForm):
    """ Форма для смены пароля."""

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2
