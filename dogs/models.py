from django.db import models
from django.conf import settings

# настройка полей, чтобы возможно было заполнить поля пустыми
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """Породы собак"""
    name = models.CharField(max_length=100, verbose_name='breed', **NULLABLE)  # `имя породы (категории)
    description = models.CharField(max_length=150, verbose_name='description', **NULLABLE)  # описание породы

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """Собаки"""
    name = models.CharField(max_length=250, verbose_name='dog_name', **NULLABLE)  # имя собаки
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')  # порода собаки
    photo = models.ImageField(upload_to='dogs/', verbose_name='image', **NULLABLE)  # фотография собаки
    birth_date = models.DateField(verbose_name='birth_date', **NULLABLE)  # дата рождения собаки
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='владелец')
    views = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.name} ({self.category})'  # собака в формате "Имя собаки (порода)"

    class Meta:
        verbose_name = 'dog'  # собака
        verbose_name_plural = 'dogs'  # собаки

    def views_count(self):
        # Каждый раз, когда собака отображается, увеличивается счетчик просмотров
        self.views += 1
        self.save()




class Parent(models.Model):
    """Родители собак"""
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="breed")
    birth_date = models.DateField(**NULLABLE, verbose_name='birth_date')

    def __str__(self) -> str:
        return f'{self.name} ({self.category})'
    
    class Meta:
        verbose_name = 'parent'
        verbose_name_plural = 'parents'