"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

"""
WSGI config для проекта config.

Он предоставляет возможность вызова WSGI в качестве переменной уровня модуля с именем `application`.

Дополнительную информацию об этом файле смотрите
в разделе https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
"""Подключение к серверу WSGI (старая механика)"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
