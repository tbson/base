from typing import List
from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import Permission, update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from services.helpers.token_utils import TokenUtils


class ResUtils:
    @staticmethod
    def get_visible_menus(groups: List[models.QuerySet]) -> List[str]:
        result: List = []
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
    def get_all_menus() -> List[str]:
        result: List = []
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
    def jwt_response_handler(token, user=None, request=None):
        from modules.account.staff.helpers.srs import (
            StaffRetrieveSr,
        )  # Handle circular import

        try:
            data = {}

            staff = user.staff
            token_context = TokenUtils.get_token_context(request)
            token_signature = TokenUtils.get_token_signature(token)

            TokenUtils.update_token_meta_data(staff, token_context, token_signature)

            data = StaffRetrieveSr(staff).data

            staff.save()
            update_last_login(None, staff.user)
            if user.is_staff:
                data["visible_menus"] = ResUtils.get_all_menus()
            else:
                data["visible_menus"] = ResUtils.get_visible_menus(user.groups.all())
            data["token"] = token

            return data
        except Exception as e:
            print(repr(e))
            error_message = _("This user didn't associate with any profile.")
            raise ValidationError({"detail": error_message})

    @staticmethod
    def get_token(headers):
        result = headers.get("Authorization", None)
        if result:
            return result.split(" ")[1]
        return ""

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
