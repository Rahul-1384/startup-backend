from rest_framework import serializers
from .models import SellDetail, BookPhoto
from .models import SellOrder

class SellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellOrder
        fields = "__all__"


class SellDetailSerializer(serializers.ModelSerializer):
   class Meta:
       model = SellDetail
       fields = '__all__'
       read_only_fields = ['user']  

   def create(self, validated_data):
       user = self.context.get('request').user
       validated_data['user'] = user
       return super().create(validated_data)

class BookPhotoSerializer(serializers.ModelSerializer):
   class Meta:
       model = BookPhoto
       fields = '__all__'

   def validate_image(self, value):
       if value.size > 10 * 1024 * 1024:
           raise serializers.ValidationError("Image size should not exceed 10 MB.")
       if not value.name.endswith(('.jpg', '.jpeg', '.png')):
           raise serializers.ValidationError("Only .jpg, .jpeg, and .png files are allowed.")
       return value