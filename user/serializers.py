from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User , Otp


from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'


class OtpInputSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)

class LoginInputSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class UserInputSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, allow_blank=True)
    uniqidentifier = serializers.CharField(required=True, allow_blank=True)
    first_name = serializers.CharField(required=True, allow_blank=True)
    last_name = serializers.CharField(required=True, allow_blank=True)
    email = serializers.EmailField(required=True, allow_blank=True)
    address = serializers.CharField(required=True, allow_blank=True)
    city = serializers.CharField(required=True, allow_blank=True)
    company = serializers.CharField(required=True, allow_blank=True)
    sheba_number = serializers.CharField(required=True, allow_blank=True)
    card_number = serializers.CharField(required=True, allow_blank=True)
    account_number = serializers.CharField(required=True, allow_blank=True)
    account_bank = serializers.CharField(required=True, allow_blank=True)

