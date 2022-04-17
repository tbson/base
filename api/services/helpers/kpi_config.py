import os
import json
from django.conf import settings


class KPIConfig:
    __result = {}

    @staticmethod
    def load():
        file_path = os.path.join(settings.BASE_DIR, "kpi.config.json")
        with open(file_path) as file:
            KPIConfig.__result = json.load(file)

    @staticmethod
    def get(key):
        return KPIConfig.__result.get(key, None)
