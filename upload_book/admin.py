from django.contrib import admin
from .models import UploadBook

@admin.register(UploadBook)
class UploadBookAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'book_author', 'user', 'original_price', 'final_price', 'status', 'created_at']
    list_filter = ['status', 'condition', 'category', 'subject', 'competitive_exam', 'boards', 'language']
    search_fields = ['book_title', 'book_author', 'user__username', 'user__email']
    readonly_fields = ['user', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('book_title', 'book_author', 'book_description', 'original_price', 'book_images')
        }),
        ('Classifications', {
            'fields': ('condition', 'category', 'subject', 'competitive_exam', 'boards', 'language')
        }),
        ('Pricing & Status', {
            'fields': ('final_price', 'discount', 'status', 'admin_notes')
        }),
        ('User Information', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """
        Override to optimize queries with related User objects.
        """
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        """
        Override to customize save behavior.
        """
        if not change and not obj.status:
            obj.status = UploadBook.Status.PENDING
        
        super().save_model(request, obj, form, change)