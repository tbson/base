from rest_framework.serializers import ModelSerializer
from ..models import Staff


class StaffSr(ModelSerializer):
    class Meta:
        model = Staff
        exclude = []

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        user = obj.user
        rep["full_name"] = obj.full_name
        rep["first_name"] = user.first_name
        rep["last_name"] = user.last_name
        rep["email"] = user.email
        rep["phone_number"] = str(user.phone_number)
        rep["groups"] = user.groups.values_list("id", flat=True)
        rep["is_active"] = obj.user.is_active
        return rep
