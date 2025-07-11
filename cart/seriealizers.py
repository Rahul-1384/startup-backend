from rest_framework import serializers
from cart.models import Cart
from sell_detail.seriealizers import SellDetailSerializer

class CartSerializer(serializers.ModelSerializer):
    book_details = SellDetailSerializer(source='book', read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'book', 'book_details', 'quantity', 'price_at_addition', 'is_active', 'total_price', 'added_at']
