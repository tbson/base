from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from services.helpers.utils import Utils
from .srs import UserSr

User = get_user_model()


class UserUtils:
    @staticmethod
    def create_user(data: dict) -> QuerySet:
        if not data.get("password"):
            data["password"] = Utils.get_random_number(12)
        sr = UserSr(data=data)
        sr.is_valid(raise_exception=True)
        user = sr.save()

        if "groups" in data:
            groups = [int(group) for group in data.get("groups", [])]
            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(user)
        return user

    @staticmethod
    def update_user(user: QuerySet, data: dict) -> QuerySet:
        user = user
        sr = UserSr(user, data=data, partial=True)
        sr.is_valid(raise_exception=True)
        user = sr.save()

        if "groups" in data:
            groups = [int(group) for group in data.get("groups", [])]
            for group in user.groups.all():
                group.user_set.remove(user)

            if list(groups):
                group_list = Group.objects.filter(id__in=groups)
                for group in group_list:
                    group.user_set.add(user)
        return user

    @staticmethod
    def get_user_by_username(username: str) -> QuerySet:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
