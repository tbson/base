from typing import List
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.conf import settings
from services.helpers.utils import Utils
from modules.configuration.variable.models import Variable
from modules.noti.verif.models import Verif, VerifLog, WhitelistTarget


class VerifUtils:
    @staticmethod
    def get_default_otp():
        return "123456"

    @staticmethod
    def get_subject():
        return _(f"{settings.APP_TITLE} - Verification code")

    @staticmethod
    def get_error_message():
        return _("You have entered incorrect OTP so many times. Please try again later")

    @staticmethod
    def send_confirmation_email(subject, to_email, verification_code, lang):
        body = render_to_string(
            f"emails/signup/{lang}.html",
            {"base_url": Utils.get_base_url(), "verification_code": verification_code},
        )

        Utils.send_email_async(subject, body, to_email)

    @staticmethod
    def send_noti_after_creating_email(subject: str, to_email: str):
        body = render_to_string(
            "emails/noti_after_creating.html",
            {"login_url": f"{Utils.get_base_url()}#/login"},
        )

        Utils.send_email_async(subject, body, to_email)

    @staticmethod
    def create(ips: List[str], target: str, lang: str = "vi"):
        try:
            in_whitelist = VerifUtils.in_whitelist(target)

            code = Utils.get_random_number()
            uid = Utils.get_uuid()

            if in_whitelist or settings.TESTING:
                code = VerifUtils.get_default_otp()

            if not settings.TESTING and not VerifUtils.write_log(ips, target):
                return (False, VerifUtils.get_error_message())

            Verif.objects.create(uid=uid, code=code, target=target)

            if in_whitelist or settings.TESTING:
                return (True, uid)

            subject = VerifUtils.get_subject()
            VerifUtils.send_confirmation_email(subject, target, code, lang)

            return (True, uid)
        except Exception:  # skipcq: whatever error
            return (False, VerifUtils.get_error_message())

    @staticmethod
    def create_again(ips: List[str], uid: str, lang: str = "vi"):
        error_message = _("Can not send OTP, please try again after 90 seconds")

        if not uid:
            return (False, error_message)

        item = Verif.objects.filter(uid=uid).order_by("-id").first()

        if not item:
            return (False, error_message)

        in_whitelist = VerifUtils.in_whitelist(item.target)

        today = datetime.now()
        diff = today - item.updated_at
        diff_seconds = diff.total_seconds()

        if diff_seconds <= settings.VERIFICATION_CODE_EXPIRED_PERIOD:
            return (False, error_message)

        if in_whitelist or settings.TESTING:
            item.code = VerifUtils.get_default_otp()
        else:
            item.code = Utils.get_random_number()

        if not VerifUtils.write_log(ips, item.target):
            return (False, VerifUtils.get_error_message())

        item.save()

        if in_whitelist or settings.TESTING:
            return (True, item.target)

        subject = VerifUtils.get_subject()
        VerifUtils.send_confirmation_email(subject, item.target, item.code, lang)

        return (True, item.target)

    @staticmethod
    def get(uid: str, code: str) -> str:
        try:
            if not uid or not code:
                return None

            item = Verif.objects.get(uid=uid, code=code)

            today = datetime.now()
            diff = today - item.updated_at
            diff_seconds = diff.total_seconds()

            if diff_seconds > settings.VERIFICATION_CODE_EXPIRED_PERIOD:
                return None

            return item
        except Verif.DoesNotExist:
            return None

    @staticmethod
    def in_whitelist(target):
        try:
            WhitelistTarget.objects.get(target=target)
            return True
        except WhitelistTarget.DoesNotExist:
            return False

    @staticmethod
    def write_log(ips: List[str], target: str):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        count = VerifLog.objects.filter(
            ips__overlap=ips,
            target=target,
            created_at__gte=start_date,
            created_at__lte=end_date,
        ).count()

        max_count = int(Variable.objects.get_value("MAX_OTP_PER_TARGET_PER_DAY", "0"))
        if count > max_count:
            return None

        return VerifLog.objects.create(ips=ips, target=target)
