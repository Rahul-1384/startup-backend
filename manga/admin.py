from django.contrib import admin
from manga.models import Manga, Review

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "added_by")  # Removed 'published_date'
    search_fields = ("title", "author")
    ordering = ("title",)  # Use an existing field for ordering

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("manga", "user", "rating", "created_at")
    search_fields = ("manga__title", "user__username")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)  # Fixed: Must be a tuple
