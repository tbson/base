from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from services.helpers.utils import Utils
from modules.account.staff.models import Staff


class Command(BaseCommand):
    help = "cmd_reset_all_password"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        queryset = Staff.objects.all()
        for item in queryset:
            user = item.user
            username = user.username
            try:
                password = Utils.get_random_number(9)
                user.password = make_password(password)
                user.save()

                subject = "Thông báo mật khẩu giao dịch trực tuyến"
                body = render_to_string(
                    "emails/reset_all_password.html",
                    {
                        "fullname": item.full_name,
                        "username": username,
                        "password": password,
                    },
                )
                print(f"[+] Sending: {username}")
                Utils.send_email(subject, body, username)
            except Exception:
                print(f"[-] Can not send: {username}")
        self.stdout.write(self.style.SUCCESS("Done!!!"))
