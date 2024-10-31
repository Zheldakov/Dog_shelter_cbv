from django.conf import settings
from django.core.cache import cache

from dogs.models import Category

def get_catiegories_cache():
    # Кеширование
    if settings.CACHE_ENABLE:
        key = 'cateegory_list'
        cateegory_list = cache.get(key)
        if cateegory_list is None:
            cateegory_list = Category.objects.all()
            cache.set(key, cateegory_list)
        else:
            cateegory_list = Category.objects.all()

        return cateegory_list
        
