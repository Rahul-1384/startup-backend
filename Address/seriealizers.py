from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'user', 'country_region', 'full_name', 'mobile_number',
            'pincode', 'flat_building_apartment', 'area_street_village',
            'landmark', 'city', 'state', 'default_address',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_mobile_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

    def create(self, validated_data):
        if validated_data.get('default_address', False):
            Address.objects.filter(user=validated_data['user'], default_address=True).update(default_address=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('default_address', False):
            Address.objects.filter(user=instance.user, default_address=True).update(default_address=False)
        return super().update(instance, validated_data)
    