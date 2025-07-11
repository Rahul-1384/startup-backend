from rest_framework import serializers
from donate.models import DonatedBook, DonationRequest

class DonatedBookSerializer(serializers.ModelSerializer):
    """Serializer for listing and adding donated books"""

    donated_by = serializers.ReadOnlyField(source="donated_by.username")  # Auto set from request user

    class Meta:
        model = DonatedBook
        fields = ["id", "title", "author", "description", "donated_by", "donated_at", "is_available"]
        read_only_fields = ["donated_by", "donated_at"]

class DonationRequestSerializer(serializers.ModelSerializer):
    """Serializer for requesting a free book"""

    user = serializers.ReadOnlyField(source="user.username")  # Auto set from request user
    book = serializers.PrimaryKeyRelatedField(queryset=DonatedBook.objects.filter(is_available=True))  # Only available books

    class Meta:
        model = DonationRequest
        fields = ["id", "user", "book", "requested_at", "status"]
        read_only_fields = ["user", "requested_at", "status"]
