"""Команда создания администратора Django (DjangoAdmin)"""
from django.core.management import BaseCommand
from django.template.defaultfilters import first

from users.models import User
from config.settings import SU_DJANGO_PASSWORD


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@web.top',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password(SU_DJANGO_PASSWORD)
        user.save()
        return 'Admin created'
