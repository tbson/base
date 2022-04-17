import importlib


class Repo:
    STAFF = ("modules.account.staff.models", "Staff")
    VARIABLE = ("modules.configuration.variable.models", "Variable")

    VERIF = ("modules.noti.verif.models", "Verif")
    VERIF_LOG = ("modules.noti.verif.models", "VerifLog")
    WHITELIST_TARGET = ("modules.noti.verif.models", "WhitelistTarget")

    @staticmethod
    def load(module_tuple):
        return getattr(importlib.import_module(module_tuple[0]), module_tuple[1])
