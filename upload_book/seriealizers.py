# serializers.py
from rest_framework import serializers
from .models import UploadBook

class UploadBookSerializer(serializers.ModelSerializer):
    """
    Serializer for regular users - can't modify admin fields
    """
    class Meta:
        model = UploadBook
        fields = [
            'id', 'book_title', 'book_author', 'book_description', 
            'original_price', 'condition', 'category', 'subject', 
            'competitive_exam', 'boards', 'language', 'book_images',
            'final_price', 'discount', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'final_price', 'discount', 'status', 'admin_notes',
            'created_at', 'updated_at'
        ]

class AdminUploadBookSerializer(serializers.ModelSerializer):
    """
    Serializer for admins - can modify all fields
    """
    class Meta:
        model = UploadBook
        fields = [
            'id', 'user', 'book_title', 'book_author', 'book_description', 
            'original_price', 'condition', 'category', 'subject', 
            'competitive_exam', 'boards', 'language', 'book_images',
            'final_price', 'discount', 'status', 'admin_notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']