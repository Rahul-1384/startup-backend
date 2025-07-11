from django.db import models
from sell_detail.models import SellDetail

class TrendingModel(models.Model):
    book = models.OneToOneField(SellDetail, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.book_title} - Trending"