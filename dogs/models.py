from django.db import models
from django.conf import settings

# настройка полей, чтобы возможно было заполнить поля пустыми
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='breed', **NULLABLE)  # `имя породы (категории)
    description = models.CharField(max_length=150, verbose_name='description', **NULLABLE)  # описание породы

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='dog_name', **NULLABLE)  # имя собаки
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')  # порода собаки
    photo = models.ImageField(upload_to='dogs/', verbose_name='image', **NULLABLE)  # фотография собаки
    birth_date = models.DateField(verbose_name='birth_date', **NULLABLE)  # дата рождения собаки

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.name} ({self.category})'  # собака в формате "Имя собаки (порода)"

    class Meta:
        verbose_name = 'dog'  # собака
        verbose_name_plural = 'dogs'  # собаки
