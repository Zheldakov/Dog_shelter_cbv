from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from dogs.models import Category, Dog
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView,  DetailView, UpdateView, DeleteView
from dogs.forms import DogForm


def index(request):
    """ Показывает главную страницу с информацией о категориях и питомниках."""
    context = {
        # отображение категорий ограничено тремя
        'object_list': Category.objects.all()[:3],
        'title': "Питомник - Главная"
    }
    return render(request, 'dogs/index.html', context)


def categories(request):
    """ Показывает страницу с информацией о всех категориях питомника."""
    context = {
        'object_list': Category.objects.all(),
        'title': "Питомник - Все наши породы"
    }
    return render(request, 'dogs/categories.html', context)


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
    extra_context ={
        'title': "Питомник - Все наши собаки",
    }
    template_name = 'dogs/dogs.html'


class DogCreateView(CreateView):
    """ Страница создания нового питомца."""
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create.html'
    success_url = reverse_lazy('dogs:list_dogs')

class DogDetailView(DeleteView):
    """ Страница детальной информации о питомца."""
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.object.pk])  # Переходим на страницу детальной информации питомца после редактирования


class DogDeleteView(DeleteView):
    """ Страница удаления питомца."""
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')  # Переходим на страницу со списком питомцев после удаления