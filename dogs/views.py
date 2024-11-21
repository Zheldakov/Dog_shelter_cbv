from lib2to3.fixes.fix_input import context

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# миксин который выполняет классы только тогда когда пользователь зарегистрированный
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.http import Http404, HttpResponseForbidden
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dogs.services import send_views_mail
from users.models import UserRoles

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm, DogAdminForm


def index(request):
    """ Показывает главную страницу с информацией о категориях и питомниках."""
    context = {
        # отображение категорий ограничено тремя
        'object_list': Category.objects.all()[:3],
        'title': "Питомник - Главная"
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - Все наши породы'
    }
    template_name = 'dogs/categories.html'


class DogDeactiveListView(LoginRequiredMixin, ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        # Показывает для тех учеток неактивных собак, и для пользователей своих неактивных собак
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """ Показывает страницу с результатами поиска собак."""
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса',
    }
    def get_queryset(self):
        query = self.request.GRT.get('q')
        object_list =Dog.objects.filter(Q(name__icontains=query))
        return object_list

class DogCategoryListView(ListView):
    """ Показывает страницу с информацией о питомцах определенной категории."""
    model = Dog
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            category_id=self.kwargs.get('pk')
        )
        # Опция которая позволяет закрыть страницу от пользователя (будет видить только своих собак)
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset


class DogListView(ListView):
    """ Показывает список всех питомцев."""
    model = Dog
    paginate_by = 3
    extra_context = {
        'title': "Питомник - Все наши собаки",
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        # Фильтр показывает только активных собак
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    """ Страница создания нового питомца."""
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        # Добавляем текущего пользователя в поле "владелец" нового питомца
        if self.request.user.role != UserRoles.USER:  # ограничивает служебные учетки
            raise PermissionDenied()
            # return HttpResponseForbidden("У вас нет прав для добавление собак") # только если ожидается перенаправление
        # form.instance.owner = self.request.user
        self.object = form.save()  # получаем объект из формы
        # добавляем владельца собаки из зарегистрированного пользователя
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    """ Страница детальной информации о питомца."""
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        # Добавляем к контексту информацию о количестве просмотров питомца
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data['title'] = f'{object.name} {object.category}'
        dog_object_increase = get_object_or_404(Dog, pk=object.pk)
        # if object.owner  != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
        if object.owner != self.request.user:
            dog_object_increase.views_count()
        if object.owner:
            object_owner_email = object.owner.email
            if dog_object_increase.views % 100 == 0 and dog_object_increase.views != 0:
                send_views_mail(dog_object_increase, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """ Страница изменения информации о питомце."""
    model = Dog
    template_name = 'dogs/update.html'

    def get_success_url(self):
        # return reverse('dogs:detail_dog', args=[self.object.pk])  # Переходим на страницу детальной информации питомца после редактирования
        # Переходим на страницу детальной информации питомца после редактирования
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        # Если питомец не принадлежит текущему пользователю или не пользователю администратор, то возбуждаем ошибку
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            # raise Http404
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        # Добавляем форму для редактирования родителей питомца
        contex_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        contex_data['formset'] = formset
        return contex_data

    def form_valid(self, form):
        # форма валидации для подставления родословной
        contex_data = self.get_context_data()
        formset = contex_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        dog_forms = {
            'admin': DogAdminForm,
            'moderator': DogForm,
            'user': DogForm,
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """ Страница удаления питомца."""
    model = Dog
    template_name = 'dogs/delete.html'
    # Переходим на страницу со списком питомцев после удаления
    success_url = reverse_lazy('dogs:list_dogs')
    # ------------------------------------------------------
    permission_required = 'dogs.delete_dog'
    # dogs.add_dog - PermissionRequiredMixin + CreateViwe
    # dogs.change_dog - PermissionRequiredMixin + UpdateViwe
    # dogs.view_dog - PermissionRequiredMixin + DetailViwe
    # ------------------------------------------------------


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()

    return redirect(reverse('dogs:list_dogs'))
