from django.contrib import admin
from dogs.models import Dog, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name') # показываем поля в списке модели
    ordering = ('pk', 'name') # сортировка по первому полю id и имени


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category') # показываем поля в списке модели
    list_filter = ('category',) # фильтрация по полям category
    ordering = ('name',) # сортировка по имени