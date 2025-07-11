from django.db import models
from django.contrib.auth import get_user_model
from rent.models import Rental
from donate.models import DonationRequest
# from sell_detail.models import SellOrder 

User = get_user_model()

class Order(models.Model):
    """Tracks orders for rented, donated, and sold books"""

    ORDER_TYPE_CHOICES = [
        ("rent", "Rent"),
        ("donate", "Donate"),
        ("sell", "Sell"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    rental = models.OneToOneField(Rental, null=True, blank=True, on_delete=models.SET_NULL, related_name="order")
    donation = models.OneToOneField(DonationRequest, null=True, blank=True, on_delete=models.SET_NULL, related_name="order")
    # sell_order = models.OneToOneField(SellOrder, null=True, blank=True, on_delete=models.SET_NULL, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.order_type} - {self.status}"
