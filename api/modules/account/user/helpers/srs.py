from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from services.helpers.utils import Utils

User = get_user_model()


class UserSr(ModelSerializer):
    class Meta:
        model = User
        exclude = []

    email = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Duplicate email")
        ]
    )

    def to_internal_value(self, data):
        phone_number = data.get("phone_number")
        phone_number = Utils.phone_to_canonical_format(phone_number)
        if not phone_number:
            phone_number = None
        data["phone_number"] = phone_number
        data["username"] = data.get("email")

        if "password" in data:
            data["password"] = make_password(data["password"])

        return super().to_internal_value(data)

    def to_representation(self, obj):
        return {
            "id": obj.pk,
            "full_name": obj.full_name,
            "is_active": obj.is_active,
            "is_staff": obj.is_staff,
        }
