from django.urls import path
from django.views.decorators.cache import cache_page,never_cache

from dogs.views import index, DogListView, DogCreateView, DogDetailView, DogUpdateView, DogDeleteView, DogCategoryListView, CategoryListView, DogDeactiveListView, dog_toggle_activity
from dogs.apps import DogsConfig

app_name = DogsConfig.name  # DogsConfig имя приложения

urlpatterns = [
    path('', cache_page(60)(index), name='index'),  # url на главную страницу  /кешируется страница 
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),  # url на страницу с информацией о всех категориях
    path('categories/<int:pk>/dogs/', DogCategoryListView.as_view(), name='category_dogs'), # url на страницу с информацией о питомцах определенной кат
    path('dogs/', DogListView.as_view(), name='list_dogs'),  # url на страницу с информацией о всех питомцах (вместо pk)
    path('dogs/dogdeactive/', DogDeactiveListView.as_view(), name='deactive_list_dogs'),  # url на страницу с информацией о всех не активных питомцах (вместо pk)
    path('dogs/create', DogCreateView.as_view(), name='create_dog'), # url на страницу создания нового питомца
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='detail_dog'),
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='update_dog'), # /не кешируется страница
    path('dogs/toggle/<int:pk>/', dog_toggle_activity, name='toggle_activity_dog'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='delete_dog')
]
