from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from services.helpers.token_utils import TokenUtils
from services.helpers.utils import Utils


class ResUtils:
    @staticmethod
    def jwt_response_handler(token, refresh_token, user):
        error_message = _("This user didn't associate with any profile.")
        try:
            data = {
                "token": token,
                "refresh_token": refresh_token,
                "user_type": "staff" if hasattr(user, "staff") else "",
            }

            if not data["user_type"]:
                raise ValidationError({"detail": error_message})

            user.refresh_token_signature = TokenUtils.get_token_signature(refresh_token)
            user.last_login = Utils.now()
            user.save()

            if user.is_staff:
                data["visible_menus"] = ResUtils.get_all_menus()
            else:
                data["visible_menus"] = ResUtils.get_visible_menus(user.groups.all())

            return data
        except Exception as e:
            print(repr(e))
            raise ValidationError({"detail": error_message})

    @staticmethod
    def get_visible_menus(groups: list[models.QuerySet]) -> list[str]:
        result = []
        for group in groups:
            permissions = group.permissions.filter(codename__startswith="view_")
            for pem in permissions:
                codename_arr = pem.codename.split("_")
                if len(codename_arr) != 2:
                    continue
                menu = codename_arr[1]
                if menu not in result:
                    result.append(menu)
        return result

    @staticmethod
    def get_all_menus() -> list[str]:
        result = []
        permissions = Permission.objects.all()
        for pem in permissions:
            codename_arr = pem.codename.split("_")
            if len(codename_arr) != 2:
                continue
            menu = codename_arr[1]
            if menu not in result:
                result.append(menu)
        return result

    @staticmethod
    def error_format(data):
        if isinstance(data, str):
            return {"detail": data}
        if isinstance(data, dict):
            return data
        return {}

    @staticmethod
    def res(item=None, extra=None, **kwargs):
        if item is None:
            item = {}
        if extra is not None:
            item["extra"] = extra
        return Response(item, **kwargs)

    @staticmethod
    def err(data, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(ResUtils.error_format(data), status=status_code)

    @staticmethod
    def error_response_to_string(error_response: dict) -> list:
        result = []
        for _status, value in error_response.items():
            if isinstance(value, str) is True and value:
                result.append(value)
            if isinstance(value, list) is True and value:
                result += value
        return result

    @staticmethod
    def get_excel_response(virtual_workbook, filename):
        response = HttpResponse(
            content=virtual_workbook,
            content_type="application/ms-excel",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


JWT_RESPONSE_HANDLER = ResUtils.jwt_response_handler
