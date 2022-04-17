from django.db.models import QuerySet
from django.conf import settings
from modules.noti.verif.helpers.model_utils import VerifModelUtils


class StaffSignals:
    @staticmethod
    def pre_save(*args, **kwargs):
        pass

    @staticmethod
    def post_save(*args, **kwargs):
        created = kwargs.get("created", False)
        if created:
            staff = kwargs.get("instance")
            StaffSignalUtilss.email_notification_after_creating(staff)

    @staticmethod
    def pre_delete(*args, **kwargs):
        pass

    @staticmethod
    def post_delete(*args, **kwargs):
        pass


class StaffSignalUtilss:
    @staticmethod
    def email_notification_after_creating(staff: QuerySet):
        if settings.STAFF_NO_EMAIL_FIX_PASSWORD:
            return
        subject = "Tạo tài khoản thành công"
        to_email = staff.email

        verif_model_utils = VerifModelUtils()
        verif_model_utils.send_noti_after_creating_email(subject, to_email)
