from typing import Dict
import pyexcel
from django.db.models import QuerySet
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ValidationError
from modules.account.helpers.group_sr import GroupSr
from services.models.repo import Repo
from .srs import StaffSr


class StaffModelUtils:
    def __init__(self, model=None):
        self.model = Repo.load(Repo.STAFF)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            phone_number = "+8490669652{}".format(i)
            if i >= 10:
                phone_number = "+849066965{}".format(i)
            test_password = "Qwerty!@#456"
            data = {
                "uid": None,
                "email": "test{}@gmail.com".format(i),
                "phone_number": phone_number,
                "first_name": f"first{i}",
                "last_name": f"last{i}",
                "password": test_password,
            }

            if save is False:
                return data

            try:
                instance = self.model.objects.get(user__username=data["email"])
            except self.model.DoesNotExist:
                instance = StaffSr(data=data)
                instance.is_valid(raise_exception=True)
                instance = instance.save()
            instance.user.password = make_password(data["password"])
            instance.user.save()
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def get(self, username: str) -> QuerySet:
        return self.model.objects.get(email=username)

    def get_info(self, staff: QuerySet) -> Dict:
        result = {"name": "", "title": ""}
        if not staff:
            return result
        title = staff.title
        result["name"] = staff.full_name
        result["title"] = getattr(title, "title", "")
        if staff.subtitle:
            result["title"] += f" ({staff.subtitle.title})"
        return result

    def get_list_group(self) -> list:
        raw_data = GroupSr(Group.objects.exclude(name="customer"), many=True).data
        return [{"value": group["id"], "label": group["name"]} for group in raw_data]
