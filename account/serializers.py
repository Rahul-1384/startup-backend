from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from account.models import User
from rest_framework.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password do not match')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before passing data
        return User.objects.create_user(**validated_data)


# User Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


# User Change Password Serializer
class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        # ✅ Check if old password is correct
        if not user.check_password(old_password):  # Fix: Use user.check_password()
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})

        # ✅ Ensure new password is different from old password
        if old_password == password:
            raise serializers.ValidationError({'password': 'New password must be different from the old password.'})

        # ✅ Confirm both new password fields match
        if password != password2:
            raise serializers.ValidationError({'password': 'Password and Confirm Password do not match.'})

        # ✅ Update the password securely
        user.set_password(password)
        user.save()

        return attrs


# User Set Password Reset Email Serializer
class SetPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:3000/api/user/reset/{uid}/{token}'
            print(link)

            # Send Email
            body = f'Click the following link to reset your password: {link}'
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise serializers.ValidationError("You are not a registered user")


# User Set Password Reset Serializer
class UserSetPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password do not match')

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError:
            raise ValidationError("Token is not valid or expired")
