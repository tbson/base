from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserSr(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Duplicate username")
        ]
    )

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)

        if "groups" in self.initial_data:
            groups = [int(group) for group in self.initial_data.get("groups", [])]
            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(instance)

        return instance

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)

        if "groups" in self.initial_data:
            groups = [int(group) for group in self.initial_data.get("groups", [])]
            for group in instance.groups.all():
                group.user_set.remove(instance)

            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(instance)

        instance.save()
        return instance
