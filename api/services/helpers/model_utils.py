from typing import List
from django.db.models import QuerySet
from .utils import Utils


class ModelUtils:
    @staticmethod
    def get(model):
        def inner(*args, **kwargs):
            try:
                if args:
                    pk = args[0]
                    if pk is not None:
                        pk = int(pk)
                    return model.objects.get(pk=pk)
                return model.objects.get(**kwargs)
            except model.DoesNotExist:
                return None

        return inner

    @staticmethod
    def empty_queryset(model):
        return model.objects.filter(pk=None)

    @staticmethod
    def queryset_to_ids(queryset: QuerySet) -> List[int]:
        return [item.pk for item in queryset]

    @staticmethod
    def get_file_field_url(obj, field):
        if file := getattr(obj, field, None):
            if hasattr(file, "url"):
                # S3 file
                if file.url.startswith("http"):
                    return file.url
                # Local file
                return Utils.get_base_url() + file.url
        return ""
