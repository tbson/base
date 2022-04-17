from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Variable
from ..helpers.srs import VariableSr


class VariableViewSet(GenericViewSet):
    _name = "variable"
    serializer_class = VariableSr
    permission_classes = (CustomPermission,)
    search_fields = ("uid", "value")

    def list(self, request):
        queryset = Variable.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = VariableSr(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Variable, pk=pk)
        serializer = VariableSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        serializer = VariableSr(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Variable, pk=pk)
        serializer = VariableSr(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(Variable, pk=pk)
        obj.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pk = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        result = Variable.objects.filter(pk__in=pk)
        if result.count() == 0:
            raise Http404
        result.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
