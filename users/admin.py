from django.contrib import admin
from users.models import User
# Регистрируем модель User в административной панели Django
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение в админ панели пользователей"""
    list_display = ('first_name', 'last_name', 'email',  'is_active', 'role', 'pk', 'is_active', 'is_staff') # Показываем поля в списке модели
    list_filter = ('last_name',) # Фильтрация по полю last_name