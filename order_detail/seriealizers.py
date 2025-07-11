from rest_framework import serializers
from order_detail.models import Order

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order tracking"""

    user = serializers.ReadOnlyField(source="user.username")  # Auto set from request user
    order_type = serializers.ChoiceField(choices=Order.ORDER_TYPE_CHOICES, read_only=True)
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ["id", "user", "order_type", "rental", "donation", "sell_order", "created_at", "updated_at", "status"]
        read_only_fields = ["user", "order_type", "created_at", "updated_at"]
