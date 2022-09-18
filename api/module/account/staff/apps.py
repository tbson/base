from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class StaffConfig(AppConfig):
    name = "module.account.staff"

    def ready(self):
        from .helper.signal import StaffSignal

        sender = self.get_model("Staff")

        pre_save.connect(StaffSignal.pre_save, sender=sender)
        post_save.connect(StaffSignal.post_save, sender=sender)
        pre_delete.connect(StaffSignal.pre_delete, sender=sender)
        post_delete.connect(StaffSignal.post_delete, sender=sender)
