from django.contrib import admin
from rent.models import RentableBook, Rental

@admin.register(RentableBook)
class RentableBookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "get_rent_price", "get_available_copies")  # Fixed field names
    search_fields = ("title", "author")

    @admin.display(description="Rent Price per Day")
    def get_rent_price(self, obj):
        return obj.rent_price_per_day

    @admin.display(description="Available Copies")
    def get_available_copies(self, obj):
        return obj.available_copies

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rental_days", "total_price", "rented_at", "expires_at", "is_paid")
    search_fields = ("user__username", "book__title")
    list_filter = ("is_paid", "expires_at")
    ordering = ("-rented_at",)  # Fixed: Must be a tuple
