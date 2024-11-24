from django.contrib import admin
from reviews.models import  Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение в админ панели"""
    list_display = ('title','dog','author','created', 'sign_of_review')
    ordering = ('created',)
    list_filter = ('dog','author',)