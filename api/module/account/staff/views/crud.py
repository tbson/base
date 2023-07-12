from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from service.framework.drf_class.custom_permission import CustomPermission

from service.request_service import RequestService
from ..models import Staff
from ..helper.util import StaffUtil
from ..helper.sr import StaffSr


class StaffViewSet(GenericViewSet):

    _name = "staff"
    permission_classes = (CustomPermission,)
    serializer_class = StaffSr
    search_fields = (
        "user__email",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
    )

    def list(self, request):
        queryset = Staff.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = StaffSr(queryset, many=True)

        result = {
            "items": serializer.data,
            "extra": {
                "options": {
                    "group": StaffUtil.get_list_group(),
                }
            },
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Staff, pk=pk)
        serializer = StaffSr(obj)
        return RequestService.res(serializer.data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        obj = StaffUtil.create_staff(request.data)
        sr = StaffSr(obj)
        return RequestService.res(sr.data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Staff, pk=pk)
        obj = StaffUtil.update_staff(obj, request.data)
        sr = StaffSr(obj)
        return RequestService.res(sr.data)

    @transaction.atomic
    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(Staff, pk=pk)
        item.delete()
        return RequestService.res(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else [int(i) for i in pk.split(",")]
        for pk in pks:
            item = get_object_or_404(Staff, pk=pk)
            item.delete()
        return RequestService.res(status=status.HTTP_204_NO_CONTENT)
