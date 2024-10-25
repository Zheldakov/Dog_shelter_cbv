"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
"""
ASGI config для проекта config.

Он предоставляет возможность вызова ASGI в качестве переменной уровня модуля с именем `application`.

Дополнительную информацию об этом файле смотрите
в разделе https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
"""Подключение к серверу ASGI (новая механика)"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
