from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView,  DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #миксин который выполняет классы только тогда когда пользователь зарегестрированный
from django.http import Http404

from dogs.models import Category, Dog
from dogs.forms import DogForm


def index(request):
    """ Показывает главную страницу с информацией о категориях и питомниках."""
    context = {
        # отображение категорий ограничено тремя
        'object_list': Category.objects.all()[:3],
        'title': "Питомник - Главная"
    }
    return render(request, 'dogs/index.html', context)


@login_required
def categories(request):
    """ Показывает страницу с информацией о всех категориях питомника."""
    context = {
        'object_list': Category.objects.all(),
        'title': "Питомник - Все наши породы"
    }
    return render(request, 'dogs/categories.html', context)

@login_required
def category_dogs(request, pk):
    """ Показывает страницу с информацией о питомцах определенной категории."""
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(ListView):
    """ Показывает список всех питомцев."""
    model = Dog
    extra_context = {
        'title': "Питомник - Все наши собаки",
    }
    template_name = 'dogs/dogs.html'


class DogCreateView(LoginRequiredMixin, CreateView):
    """ Страница создания нового питомца."""
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        # Добавляем текущего пользователя в поле "владелец" нового питомца
        # form.instance.owner = self.request.user
        self.object = form.save # получаем объект из формы
        self.object.owner = self.request.user # добавляем владельца собаки из зарегистрированого пользователя
        self.object.save()
        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    """ Страница детальной информации о питомца."""
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """ Страница изменения информации о питомце."""
    model = Dog
    form_class = DogForm
    template_name = 'dogs/update.html'

    def get_success_url(self):
        # return reverse('dogs:detail_dog', args=[self.object.pk])  # Переходим на страницу детальной информации питомца после редактирования
        # Переходим на страницу детальной информации питомца после редактирования
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])
    
    def get_object(self, queryset=None):
        # Если питомец не принадлежит текущему пользователю или не пользователю администратор, то возбуждаем ошибку
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

class DogDeleteView(DeleteView):
    """ Страница удаления питомца."""
    model = Dog
    template_name = 'dogs/delete.html'
    # Переходим на страницу со списком питомцев после удаления
    success_url = reverse_lazy('dogs:list_dogs')
