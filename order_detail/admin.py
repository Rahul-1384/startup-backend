from django.contrib import admin
from order_detail.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "order_type", "status", "created_at", "updated_at")
    search_fields = ("user__username", "order_type", "status")
    list_filter = ("order_type", "status", "created_at")
    ordering = ("-created_at",)
