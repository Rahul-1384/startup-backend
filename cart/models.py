from django.db import models
from account.models import User
from sell_detail.models import SellDetail

# models.py
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    book = models.ForeignKey(SellDetail, on_delete=models.CASCADE, to_field='book_id', related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)  
    price_at_addition = models.PositiveIntegerField()  
    is_active = models.BooleanField(default=True)  
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    @property
    def total_price(self):
        return self.quantity * self.price_at_addition

    def __str__(self):
        return f"{self.user.email} - {self.book.book_title} (Quantity: {self.quantity}, Total: {self.total_price})"
    



