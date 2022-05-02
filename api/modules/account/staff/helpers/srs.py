from rest_framework.serializers import ModelSerializer
from modules.account.user.helpers.srs import UserSr
from ..models import Staff


class StaffSr(ModelSerializer):
    class Meta:
        model = Staff
        exclude = []

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        user = obj.user
        rep["full_name"] = obj.full_name
        rep["email"] = user.email
        rep["phone_number"] = str(user.phone_number)
        rep["is_active"] = obj.user.is_active
        rep["user"] = UserSr(obj.user).data
        return rep
