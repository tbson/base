from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class StaffConfig(AppConfig):
    name = "modules.account.staff"

    def ready(self):
        from .helpers.signals import StaffSignals

        sender = self.get_model("Staff")

        pre_save.connect(StaffSignals.pre_save, sender=sender)
        post_save.connect(StaffSignals.post_save, sender=sender)
        pre_delete.connect(StaffSignals.pre_delete, sender=sender)
        post_delete.connect(StaffSignals.post_delete, sender=sender)
