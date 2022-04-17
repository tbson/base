import base64
import json
import requests
from django.conf import settings
from services.helpers.utils import Utils


class SpeedSMS:
    @staticmethod
    def send_sms(subject: str, target: str, code: str) -> str:
        if not Utils.check_valid_phone_number(target):
            return ""

        target = target[1:]
        branch_name = settings.SPEED_SMS_BRANCH_NAME
        token = "{}:x".format(settings.SPEED_SMS_ACCESS_TOKEN)
        token = base64.b64encode(token.encode())
        token = token.decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(token),
        }
        url = "https://api.speedsms.vn/index.php/sms/send/"
        data = {
            "to": [target],
            "content": "{}: {}".format(subject, code),
            "sms_type": 3,
            "sender": branch_name,
        }
        requests.post(url, data=json.dumps(data), headers=headers)

    @staticmethod
    def send_sms_async(*args):
        Utils.async_exec(SpeedSMS.send_sms, *args)
