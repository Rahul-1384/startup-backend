from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class RentableBook(models.Model):
    """Books available for rent (Listed by Admins)"""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="rent_books/covers/")
    pdf_file = models.FileField(upload_to="rent_books/pdfs/")
    daily_rental_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per day
    listed_at = models.DateTimeField(auto_now_add=True)
    listed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rented_books")

    def __str__(self):
        return self.title

class Rental(models.Model):
    """Tracks book rentals by users"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rentals")
    book = models.ForeignKey(RentableBook, on_delete=models.CASCADE, related_name="rental_orders")
    rented_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    rental_days = models.PositiveIntegerField()  # User-defined rental period
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Auto-calculated price
    is_paid = models.BooleanField(default=False)  # Payment status

    def save(self, *args, **kwargs):
        """Automatically set expiry date and calculate total price"""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=self.rental_days)  # Ensure correct expiry calculation
        self.total_price = self.book.daily_rental_price * self.rental_days  # Calculate price
        super().save(*args, **kwargs)

    def has_expired(self):
        """Check if rental period is over"""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} rented {self.book.title} for {self.rental_days} days (Expires: {self.expires_at})"
