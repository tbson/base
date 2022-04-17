from django.db import models
from django.contrib.auth.models import Permission
from services.helpers.utils import Utils


class RoleModelUtils:
    def seeding(
        self, index: int, single: bool = False, save: bool = True
    ) -> models.QuerySet:
        from .srs import RoleSr

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            data = {
                "name": "name{}".format(i),
            }
            if save is False:
                return data

            instance = RoleSr(data=data)
            instance.is_valid(raise_exception=True)
            instance = instance.save()
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def all_permissions(self) -> dict:
        result: list = []
        permissions = Permission.objects.exclude(
            content_type__model__in=[
                "logentry",
                "token",
                "session",
                "contenttype",
                "user",
                "permission",
                "veriflog",
                "verif",
                "whitelisttarget",
                "tokenproxy",
                "device",
                "notification",
                "quotavaluelog",
            ]
        ).order_by("content_type__model")
        for pem in permissions:
            result.append(
                Utils.get_transfer_data_source(pem.pk, pem.content_type.model, pem.name)
            )
        return result

    def group_content_type(self, permissions: list) -> dict:
        result: dict = {}
        for pem in permissions:
            short_pem = {
                "id": pem["id"],
                "title": pem["title"],
            }
            content_type = str(pem["type"])
            if content_type not in result:
                result[content_type] = [short_pem]
            else:
                result[content_type].append(short_pem)
        return result
