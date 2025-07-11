from rest_framework import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rent.models import RentableBook, Rental

class RentableBookSerializer(serializers.ModelSerializer):
    """Serializer for books available for rent (Admins list books)"""

    class Meta:
        model = RentableBook
        fields = "__all__"

class RentalSerializer(serializers.ModelSerializer):
    """Serializer for renting a book (User selects rental duration)"""

    user = serializers.ReadOnlyField(source="user.username")  
    book = serializers.PrimaryKeyRelatedField(queryset=RentableBook.objects.all())  
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  
    is_expired = serializers.SerializerMethodField()  

    class Meta:
        model = Rental
        fields = ["id", "user", "book", "rental_days", "total_price", "rented_at", "expires_at", "is_paid", "is_expired"]
        read_only_fields = ["total_price", "rented_at", "expires_at", "is_paid", "is_expired"]

    def get_is_expired(self, obj):
        """Returns True if the rental period has expired"""
        return timezone.now() > obj.expires_at

    def validate_rental_days(self, value):
        """Ensure rental_days is at least 1 day"""
        if value < 1:
            raise ValidationError("Rental duration must be at least 1 day.")
        return value

    def create(self, validated_data):
        """Automatically set expiry and total price on rental creation"""
        request = self.context.get("request")  
        validated_data["user"] = request.user  

        # Ensure rental_days is valid
        rental_days = validated_data.get("rental_days", 1)

        # Get book instance
        book = validated_data["book"]

        # Calculate price and expiry date
        validated_data["total_price"] = book.rent_price_per_day * rental_days
        validated_data["expires_at"] = timezone.now() + timezone.timedelta(days=rental_days)

        rental = Rental.objects.create(**validated_data)
        return rental
