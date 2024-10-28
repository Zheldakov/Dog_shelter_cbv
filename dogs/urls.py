from django.urls import path
from dogs.views import index, categories, category_dogs, dog_detail_view, dog_update_view, dog_delete_view, DogListView, DogCreateView
from dogs.apps import DogsConfig

app_name = DogsConfig.name  # DogsConfig имя приложения

urlpatterns = [
    path('', index, name='index'),  # url на главную страницу
    path('categories/', categories, name='categories'),  # url на страницу с информацией о всех категориях
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'), # url на страницу с информацией о питомцах определенной кат
    path('dogs/', DogListView.as_view(), name='list_dogs'),  # url на страницу с информацией о всех питомцах (вместо pk)
    path('dogs/create',DogCreateView.as_view(), name='create_dog'), # url на страницу создания нового питомца
    path('dogs/detail/<int:pk>/',dog_detail_view, name='detail_dog'),
    path('dogs/update/<int:pk>/',dog_update_view, name='update_dog'),
    path('dogs/delete/<int:pk>/',dog_delete_view, name='delete_dog')
]
