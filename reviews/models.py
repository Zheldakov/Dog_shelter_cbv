from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    # Модель отзыва
    title = models.CharField(max_length=150, verbose_name='title')  # title
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')  # slug
    content = models.TextField(verbose_name='Содержимое')  # content
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)  # datetime
    sign_of_review = models.BooleanField(default=True, verbose_name="Активный")  # sign_of_review
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                               verbose_name='Автор')  # author
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, verbose_name='Собака')  # Dog

    def __str__(self):
        # Возвращает заголовок отзыва в виде строки
        return f'{self.title}'

    def get_absolute_url(self):
        # Возвращает абсолютный URL для страницы детального отзыва
        return reverse('reviews:detail_review', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'