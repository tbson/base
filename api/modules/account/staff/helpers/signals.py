from django.db.models import QuerySet
from modules.noti.verif.helpers.utils import VerifUtils


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
        subject = "Tạo tài khoản thành công"
        to_email = staff.user.email

        VerifUtils.send_noti_after_creating_email(subject, to_email)
