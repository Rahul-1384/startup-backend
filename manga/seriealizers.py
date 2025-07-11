from rest_framework import serializers
from manga.models import Manga, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class MangaSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField()  # Show uploader's username

    class Meta:
        model = Manga
        fields = "__all__"  # Includes all fields

    def create(self, validated_data):
        """
        Create a new manga entry.
        Ensure only admins can upload manga.
        """
        request = self.context.get("request")
        if request and not request.user.is_admin:
            raise serializers.ValidationError("Only admins can upload manga.")
        validated_data["added_by"] = request.user  # Assign uploader
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update manga details.
        Only admins can modify manga entries.
        """
        request = self.context.get("request")
        if request and not request.user.is_admin:
            raise serializers.ValidationError("Only admins can update manga.")
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    manga = serializers.PrimaryKeyRelatedField(queryset=Manga.objects.all())

    class Meta:
        model = Review
        fields = "__all__"

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """
        Create a new review.
        Ensure users cannot review the same manga multiple times.
        """
        request = self.context.get("request")
        user = request.user if request else None
        manga = validated_data.get("manga")

        if Review.objects.filter(user=user, manga=manga).exists():
            raise serializers.ValidationError("You have already reviewed this manga.")

        validated_data["user"] = user  # Assign review to user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update a review.
        Ensure only the original reviewer can modify their review.
        """
        request = self.context.get("request")
        if request and instance.user != request.user:
            raise serializers.ValidationError("You can only update your own reviews.")
        return super().update(instance, validated_data)
