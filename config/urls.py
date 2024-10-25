"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
Настройка URL-адресов для проекта config.

Список `urlpatterns` перенаправляет URL-адреса в представления. Для получения дополнительной информации, пожалуйста, смотрите:
 https://docs.djangoproject.com/en/5.0/topics/http/urls/
Примеры:
Функциональные представления
 1. Добавьте импорт: из my_app импортируйте представления
 2. Добавьте URL-адрес в urlpatterns: path(", views.home, name="home")
Представления на основе классов
 1. Добавьте импорт: из other_app.views импортируйте Home
 2. Добавьте URL-адрес в urlpatterns: path(", Home.as_view(), name="home")
Включая другой URLconf
 1. Импортируйте функцию include(): из django.urls импортируйте include, path
 2. Добавьте URL-адрес в urlpatterns: path('blog/', include('blog.urls'))
"""
"""Отслеживание url-адресов"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# urls для административной панели Django
urlpatterns = [
                  path('admin/', admin.site.urls),  # URL для административной панели Django
                  path('', include('dogs.urls', namespace='dogs')),  # URL для приложения dogs
                  path('users/', include('users.urls', namespace='users')),  # URL для приложения users)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Добавляем медиафайлы
