from django.urls import path
from django.views.decorators.cache import cache_page,never_cache

from dogs.views import index, categories, DogListView, DogCreateView, DogDetailView, DogUpdateView, DogDeleteView, DogCategoryListView
from dogs.apps import DogsConfig

app_name = DogsConfig.name  # DogsConfig имя приложения

urlpatterns = [
    # path('', index, name='index'),  # url на главную страницу
    path('', cache_page(60)(index), name='index'),  # url на главную страницу  /кешируется страница
    # path('categories/', categories, name='categories'),  # url на страницу с информацией о всех категориях
    path('categories/', cache_page(60)(categories), name='categories'),  # url на страницу с информацией о всех категориях
    path('categories/<int:pk>/dogs/', DogCategoryListView.as_view(), name='category_dogs'), # url на страницу с информацией о питомцах определенной кат
    path('dogs/', DogListView.as_view(), name='list_dogs'),  # url на страницу с информацией о всех питомцах (вместо pk)
    path('dogs/create',DogCreateView.as_view(), name='create_dog'), # url на страницу создания нового питомца
    path('dogs/detail/<int:pk>/',DogDetailView.as_view(), name='detail_dog'),
    # path('dogs/update/<int:pk>/', DogUpdateView.as_view(), name='update_dog'),
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='update_dog'), # /не кешируется страница
    path('dogs/delete/<int:pk>/',DogDeleteView.as_view(), name='delete_dog')
]
