from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class DonatedBook(models.Model):
    """Model for books donated by users or admins"""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    donated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donated_books")
    donated_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - Donated by {self.donated_by.username}"

class DonationRequest(models.Model):
    """Model for requesting a free book"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donation_requests")
    book = models.ForeignKey(DonatedBook, on_delete=models.CASCADE, related_name="requests")
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )

    def __str__(self):
        return f"{self.user.username} requested {self.book.title} - {self.status}"
