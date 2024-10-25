import random
import string

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import reverse, render, redirect

from django.contrib.auth.views import LoginView, PasswordChangeDoneView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    """ Регистрация пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'user/register_user.html'


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


def user_logout_view(request):
    # выход из системы
    logout(request)
    return redirect('dogs:index')


class UserUpdateView(UpdateView):
    """ Изменение профиля пользователя."""
    model = User
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def user_update_view(request):
    # изменение профиля пользователя
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:profile_user'))
    user_name = user_object.first_name
    context = {
        'user_object': user_object,
        'title': f'Изменение профиля {user_name}',
        'form': UserUpdateForm(instance=user_object),
    }
    return render(request, 'user/update_user.html', context)


@login_required
def user_change_password_view(request):
    # изменение пароля пользователя
    user_object = request.user
    form = UserPasswordChangeForm(user_object, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, "Пароль был успешно изменен")
            return HttpResponseRedirect(reverse('users:profile_user'))
        else:
            messages.error(
                request, "Пароль не был изменен. Проверьте введенные данные.")
    context = {'form': form}
    return render(request, 'user/change_password_user.html', context)


@login_required
def user_generate_new_password(request):
    # генерация нового пароля и отправка его на почту
    new_password = ''.join(random.sample(
        (string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
