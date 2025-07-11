from rest_framework import serializers
from Trending.models import TrendingModel
from sell_detail.seriealizers import SellDetailSerializer

class TrendingSerializer(serializers.ModelSerializer):
    book_details = SellDetailSerializer(source='book', read_only=True)

    class Meta:
        model = TrendingModel
        fields = ['id', 'book', 'book_details', 'rank', 'created_at']