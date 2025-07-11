from django.contrib import admin
from sell_detail.models import SellDetail, BookPhoto,SellOrder

@admin.register(SellOrder)
class SellOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "seller", "book", "order_status", "created_at")
    list_filter = ("order_status",)
    search_fields = ("buyer__username", "seller__username", "book__book_title")

@admin.register(SellDetail)
class SellDetailAdmin(admin.ModelAdmin):
    list_display = [
        'book_title', 'book_author', 'book_AI_price',  # Remove 'book_expected_price'
    ]

@admin.register(BookPhoto)
class BookPhotoAdmin(admin.ModelAdmin):
    list_display = ('sell_detail', 'created_at')
    search_fields = ('sell_detail__book_title',)
    list_filter = ('created_at',)