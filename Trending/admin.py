from django.contrib import admin
from Trending.models import TrendingModel

@admin.register(TrendingModel)
class TrendingModelAdmin(admin.ModelAdmin):
    list_display = ('book', 'rank', 'created_at')
    search_fields = ('book__book_title',)
    list_filter = ('rank', 'created_at')
    ordering = ('rank',)
