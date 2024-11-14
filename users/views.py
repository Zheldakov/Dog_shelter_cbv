import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import reverse, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    """ Регистрация пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'user/register_user.html'

    def form_valid(self, form):
        # переписываем form_valid для отправки письма при регестрации
        self.object = form.save()  # получаем объект из формы
        send_register_email(self.object.email)  # отправляем письмо  на почту объекта
        return super().form_valid(form)


class UserLoginView(LoginView):
    """ Логин пользователя."""
    template_name = 'user/login_user.html'
    form_class = UserLoginForm


class UserProfileView(UpdateView):
    """ Изменение профиля пользователя."""
    model = User
    form_class = UserForm
    template_name = 'user/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserLogoutView(LogoutView):
    """ Выход пользователя."""

    template_name = 'user/logout_user.html'


class UserUpdateView(UpdateView):
    """ Изменение профиля пользователя."""
    model = User
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """ Изменение пароля пользователя."""
    form_class = UserPasswordChangeForm
    template_name = 'user/change_password_user.html'
    success_url = reverse_lazy('users:profile_user')


class UserListView(LoginRequiredMixin, ListView):
    """ Список всех заводчиков."""
    model = User
    extra_context = {
        'title': 'Питомник. Все наши заводчики'
    }
    template_name = 'user/users.html'

    def get_queryset(self):
        # фильтр показывает только активных пользователей
        queryset = super().queryset.filtr(is_active=True)
        return queryset


@login_required
def user_generate_new_password(request):
    # генерация нового пароля и отправка его на почту
    new_password = ''.join(random.sample(
        (string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
