from custom_type import query_obj
from module.noti.verif.helper.util import VerifUtil


class StaffSignal:
    @staticmethod
    def pre_save(*args, **kwargs):
        pass

    @staticmethod
    def post_save(*args, **kwargs):
        if kwargs.get("created", False):
            staff = kwargs.get("instance")
            StaffSignalutil.email_notification_after_creating(staff)

    @staticmethod
    def pre_delete(*args, **kwargs):
        pass

    @staticmethod
    def post_delete(*args, **kwargs):
        pass


class StaffSignalutil:
    @staticmethod
    def email_notification_after_creating(staff: query_obj):
        subject = "Tạo tài khoản thành công"
        to_email = staff.user.email

        VerifUtil.send_noti_after_creating_email(subject, to_email)
