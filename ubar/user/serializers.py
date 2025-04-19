from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.hashers import make_password
from user.validators import phone_validator
from user.models.user import User


class LoginObtainOTPInputSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)

    def validate_phone(self, phone: str) -> str:
        return phone_validator(phone=phone)


class LoginVerifyOTPInputSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)
    code = serializers.CharField(max_length=11, min_length=11)


class LoginVerifyPasswordInputSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)
    password = serializers.CharField(
        max_length=settings.PASSWORD_MAX_LENGTH,
        min_length=settings.PASSWORD_MIN_LENGTH,
    )


class UsersSerializer(serializers.ModelSerializer):
    raw_password = serializers.CharField(
        required=False,
        max_length=settings.PASSWORD_MAX_LENGTH,
        min_length=settings.PASSWORD_MIN_LENGTH,
    )
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "family",
            "suspended_at",
            "phone",
            "raw_password",
            "has_password",
            "created_at",
            "updated_at",
            "limited_at",
        ]
        read_only_fields = [
            "id",
            "phone",
            "suspended_at",
            "has_password",
            "created_at",
            "updated_at",
            "limited_at",
        ]

    def get_has_password(self, obj):
        return bool(obj.password)

    def create(self, validated_data):
        raw_password = validated_data.pop("raw_password", None)
        user = super().create(validated_data=validated_data)
        if raw_password:
            user.hash_password(raw_password=raw_password)
            user.save()
        return user

    def update(self, instance, validated_data):
        raw_password = validated_data.pop("raw_password", None)
        user = super().update(instance=instance, validated_data=validated_data)
        if raw_password:
            user.hash_password(raw_password=raw_password)
            user.save()
        return user


class LoginVerifyOTPInputSerializer(serializers.Serializer):
    code = serializers.IntegerField(
        max_value=settings.OTP_UPPER_BOUND,
        min_value=settings.OTP_LOWER_BOUND,
    )

class ProfileInputSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    family = serializers.CharField()

    def validate_phone(self, phone: str) -> str:
        return phone_validator(phone=phone)