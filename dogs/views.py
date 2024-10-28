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


@login_required
def dog_update_view(request, pk):
    """ Страница редактирования питомца."""
    # dog_object = Dog.objects.get(pk=pk)  # Получаем питомца из базы по(тоже что и ниже)
    # Получаем питомца из базы по pk
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES,
                       instance=dog_object)  # Валидация формы
        if form.is_valid():  # Если форма валидна, сохраняем данные
            dog_object = form.save()  # Сохраняем питомца в базе
            dog_object.save()  # Сохраняем питомца в базе
            return HttpResponseRedirect(reverse('dogs:detail_dog', args={pk: pk}))
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object),
        # Заголовок страницы редактирования
        'title': f'Редактирование информации о собаке {dog_object.name}'
    }
    # Отображаем форму создания питомца
    return render(request, 'dogs/update.html', context)


def dog_delete_view(request, pk):
    # Получаем питомца из базы по pk
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':  # Если запрос POST
        dog_object.delete()  # Удаляем питомца из базы
        # Переходим на страницу со списком питомцев
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object}, )  # Отображаем страницу подтверждения удаления
