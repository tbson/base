from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group as Role

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from services.drf_classes.custom_permission import CustomPermission
from services.drf_classes.custom_pagination import NoPaginationStatic
from services.helpers.res_utils import ResUtils

from ..helpers.srs import RoleSr
from ..helpers.model_utils import RoleModelUtils


class RoleViewSet(GenericViewSet):
    def __init__(self, *args, **kwargs):
        self.model_utils = RoleModelUtils()

    _name = "role"
    serializer_class = RoleSr
    permission_classes = (CustomPermission,)
    pagination_class = None
    search_fields = ("name",)

    def list(self, request):
        queryset = Role.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = RoleSr(queryset, many=True)
        result = {
            "items": serializer.data,
            "extra": {"permissions": self.model_utils.all_permissions()},
        }
        return NoPaginationStatic.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Role, pk=pk)
        serializer = RoleSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        serializer = RoleSr(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Role, pk=pk)
        serializer = RoleSr(obj, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(Role, pk=pk)
        obj.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pk = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        result = Role.objects.filter(pk__in=pk)
        if result.count() == 0:
            raise Http404
        result.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
