from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'mobile_number', 'pincode', 'city', 'state', 
        'country_region', 'default_address', 'created_at'
    )
    list_filter = ('country_region', 'state', 'default_address', 'created_at')
    search_fields = ('full_name', 'mobile_number', 'city', 'pincode')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')