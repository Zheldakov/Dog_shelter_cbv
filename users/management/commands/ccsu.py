"""Команда создания администратора Django (DjangoAdmin)"""
from django.core.management import BaseCommand
from django.template.defaultfilters import first

from users.models import User
from config.settings import SU_DJANGO_PASSWORD


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = User.objects.create(
            email='admin@web.top',
            first_name='Admin',
            last_name='Adminov',
            role = 'admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        admin.set_password(SU_DJANGO_PASSWORD)
        admin.save()
    print('Admin created')
    
    moderator = User.objects.create(
        email='moderator@web.top',
        first_name='Moderator',
        last_name='Moderator',
        role='moderator',
        is_staff=True,
        is_superuser=False,
        is_active=True
    )
    moderator.set_password(SU_DJANGO_PASSWORD)
    moderator.save()
    print('Moderator created')
    
    user = User.objects.create(
        email='user@web.top',
        first_name='User',
        last_name='User',
        role='user',
        is_staff=True,
        is_superuser=False,
        is_active=True
    )
    user.set_password(SU_DJANGO_PASSWORD)
    user.save()
    print('User created')
