from django.db.models import QuerySet
from services.models.repo import Repo
from .srs import VariableSr
from ..consts import SettingVariables


class VariableModelUtils:
    def __init__(self, model=None):
        self.model = Repo.load(Repo.VARIABLE)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            data = {"uid": "uid{}".format(i), "value": "value{}".format(i)}
            if save is False:
                return data
            try:
                instance = self.model.objects.get(uid=data["uid"])
            except self.model.DoesNotExist:
                instance = VariableSr(data=data)
                instance.is_valid(raise_exception=True)
                instance = instance.save()
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def settings_seeding(self, print_result):
        obj = SettingVariables()
        attributes = [
            a
            for a in dir(obj)
            if not a.startswith("__") and not callable(getattr(obj, a))
        ]
        variable_model_utils = VariableModelUtils()
        for uid in attributes:
            try:
                self.model.objects.get(uid=uid)
            except self.model.DoesNotExist:
                value = getattr(SettingVariables, uid)
                print_result(uid, value)
                variable_model_utils.set(uid, value)

    def get(self, uid: str, default_value: str = "") -> str:
        try:
            item = self.model.objects.get(uid=uid)
            return item.value
        except self.model.DoesNotExist:
            if hasattr(SettingVariables, uid):
                return getattr(SettingVariables, uid)
            return default_value

    def set(self, uid: str, value: str) -> QuerySet:

        try:
            item = self.model.objects.get(uid=uid)
            item.value = value
            item.save()
            return item
        except self.model.DoesNotExist:
            return self.model.objects.create(uid=uid, value=value)
