from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from services.helpers.utils import Utils
from modules.account.helpers.group_sr import GroupSr
from modules.account.helpers.user_sr import UserSr
from ..models import Staff


class StaffSr(ModelSerializer):
    class Meta:
        model = Staff
        exclude = ["user"]

    groups = SerializerMethodField()
    group_labels = SerializerMethodField()

    def to_internal_value(self, obj):
        phone_number = obj.get("phone_number")
        phone_number = Utils.phone_to_canonical_format(phone_number)
        if not phone_number:
            phone_number = None
        obj["phone_number"] = phone_number
        return super().to_internal_value(obj)

    def to_representation(self, obj):

        obj = Staff.objects.get(pk=obj.pk)
        rep = super().to_representation(obj)
        rep["full_name"] = obj.full_name
        rep["is_active"] = obj.user.is_active
        rep["is_active_label"] = "YES" if obj.user.is_active else ""
        return rep

    def get_groups(self, obj):
        groups = GroupSr(obj.user.groups.all(), many=True).data
        return map(lambda group: group["id"], groups)

    def get_group_labels(self, obj):
        groups = GroupSr(obj.user.groups.all(), many=True).data
        result = [group["name"] for group in groups]
        return ", ".join(result)

    def create(self, validated_data):
        email = validated_data.get("email", None)

        user_sr = UserSr(data={"username": email.lower()})
        user_sr.is_valid(raise_exception=True)

        user = user_sr.save()
        is_active = self.initial_data.get("is_active")
        if is_active is not None:
            user.is_active = is_active
            user.save()

        password = settings.STAFF_NO_EMAIL_FIX_PASSWORD
        if password:
            user.password = make_password(password)
            user.save()

        if "groups" in self.initial_data:
            groups = [int(group) for group in self.initial_data.get("groups", [])]
            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(user)

        data = {**validated_data, **{"user_id": user.pk}}
        return Staff.objects.create(**data)

    def update(self, instance, validated_data):
        for key in ["title", "subtitle", "title_level"]:
            if key in validated_data:
                validated_data["{}_id".format(key)] = validated_data[key]

        email = validated_data.get("email", "").lower()

        if email:
            validated_data["email"] = email

        instance.__dict__.update(validated_data)

        if "groups" in self.initial_data:
            groups = [int(group) for group in self.initial_data.get("groups", [])]
            for group in instance.user.groups.all():
                group.user_set.remove(instance.user)

            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(instance.user)

        is_active = self.initial_data.get("is_active")
        if is_active is not None:
            instance.user.is_active = is_active
            instance.user.save()

        if email:
            instance.user.username = email
            instance.user.save()

        instance.save()
        return instance


class StaffRetrieveSr(StaffSr):
    class Meta(StaffSr.Meta):
        exclude = [
            "created_at",
            "updated_at",
            "token_context",
            "token_signature",
            "token_refresh_limit",
            "user",
        ]
