from django.contrib import admin
from users.models import User
# Регистрируем модель User в административной панели Django
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',  'is_active', 'role', 'pk', 'is_active') # Показываем поля в списке модели
    list_filter = ('last_name',) # Фильтрация по полю last_name