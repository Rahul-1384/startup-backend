from django.contrib import admin
from donate.models import DonatedBook, DonationRequest

@admin.register(DonatedBook)
class DonatedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "donated_by", "donated_at", "is_available")
    search_fields = ("title", "author", "donated_by__username")
    list_filter = ("is_available", "donated_at")
    ordering = ("-donated_at",)

@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "requested_at", "status")
    search_fields = ("user__username", "book__title")
    list_filter = ("status", "requested_at")
    ordering = ("-requested_at",)
