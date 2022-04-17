from typing import List
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.conf import settings
from services.models.repo import Repo
from services.helpers.utils import Utils
from services.sms.speed_sms import SpeedSMS


class VerifModelUtils:
    default_whitelist_code = settings.DEFAULT_WHITELIST_OTP

    def __init__(self, model=None):
        self.model = Repo.load(Repo.VERIF)
        self.verif_log_model = Repo.load(Repo.VERIF_LOG)
        self.whitelist_target_model = Repo.load(Repo.WHITELIST_TARGET)
        self.variable_model = Repo.load(Repo.VARIABLE)

    def get_subject(self):
        return _("{} - Verification code".format(settings.APP_TITLE))

    def get_error_message(self):
        return _("You have entered incorrect OTP so many times. Please try again later")

    def send_confirmation_email(self, subject, to_email, verification_code, lang):
        body = render_to_string(
            "emails/signup/{}.html".format(lang),
            {"base_url": Utils.get_base_url(), "verification_code": verification_code},
        )

        Utils.send_email_async(subject, body, to_email)

    def send_noti_after_creating_email(self, subject: str, to_email: str):
        body = render_to_string(
            "emails/noti_after_creating.html",
            {"login_url": "{}#/login".format(Utils.get_base_url())},
        )
        Utils.send_email_async(subject, body, to_email)

    def create(self, ips: List[str], target: str, lang: str = "vi"):
        try:
            in_whitelist = self.in_whitelist(target)

            code = Utils.get_random_number()
            uid = Utils.get_uuid()

            if in_whitelist or settings.TESTING:
                code = self.default_whitelist_code

            if not settings.TESTING and not self.write_log(ips, target):
                return (False, self.get_error_message())

            self.model.objects.create(uid=uid, code=code, target=target)

            if in_whitelist or settings.TESTING:
                return (True, uid)

            subject = self.get_subject()
            if "@" in target:
                self.send_confirmation_email(subject, target, code, lang)
            else:
                SpeedSMS.send_sms_async(subject, target, code)

            return (True, uid)
        except Exception:
            return (False, self.get_error_message())

    def create_again(self, ips: List[str], uid: str, lang: str = "vi"):
        error_message = _("Can not send OTP, please try again after 90 seconds")

        if not uid:
            return (False, error_message)

        item = self.model.objects.filter(uid=uid).order_by("-id").first()

        if not item:
            return (False, error_message)

        in_whitelist = self.in_whitelist(item.target)

        today = datetime.now()
        diff = today - item.updated_at
        diff_seconds = diff.total_seconds()

        if diff_seconds <= settings.VERIFICATION_CODE_EXPIRED_PERIOD:
            return (False, error_message)

        if in_whitelist or settings.TESTING:
            item.code = self.default_whitelist_code
        else:
            item.code = Utils.get_random_number()

        if not self.write_log(ips, item.target):
            return (False, self.get_error_message())

        item.save()

        if in_whitelist or settings.TESTING:
            return (True, item.target)

        subject = self.get_subject()
        if "@" in item.target:
            self.send_confirmation_email(subject, item.target, item.code, lang)
        else:
            SpeedSMS.send_sms_async(subject, item.target, item.code)

        return (True, item.target)

    def get(self, uid: str, code: str) -> str:
        try:
            if not uid or not code:
                return None

            item = self.model.objects.get(uid=uid, code=code)

            today = datetime.now()
            diff = today - item.updated_at
            diff_seconds = diff.total_seconds()

            if diff_seconds > settings.VERIFICATION_CODE_EXPIRED_PERIOD:
                return None

            return item
        except self.model.DoesNotExist:
            return None

    def in_whitelist(self, target):
        try:
            self.whitelist_target_model.objects.get(target=target)
            return True
        except self.whitelist_target_model.DoesNotExist:
            return False

    def write_log(self, ips: List[str], target: str):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        count = self.verif_log_model.objects.filter(
            ips__overlap=ips,
            target=target,
            created_at__gte=start_date,
            created_at__lte=end_date,
        ).count()

        max_count = int(
            self.variable_model.objects.get_value("MAX_OTP_PER_TARGET_PER_DAY", "0")
        )
        if count > max_count:
            return None

        item = self.verif_log_model.objects.create(ips=ips, target=target)

        return item
