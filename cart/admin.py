from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'price_at_addition', 'total_price', 'is_active', 'added_at')
    search_fields = ('user__email', 'book__book_title')
    list_filter = ('is_active', 'added_at')
