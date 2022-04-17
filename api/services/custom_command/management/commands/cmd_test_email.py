from django.core.management.base import BaseCommand
from services.helpers.utils import Utils


class Command(BaseCommand):
    help = "cmd_test_email"

    def add_arguments(self, parser):
        parser.add_argument("target", type=str, help="Email address")

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[+] Start..."))
        subject = "Test subject"
        body = "Test body"
        target = options.get("target")
        self.stdout.write(self.style.SUCCESS("[*] Sending email to: {}".format(target)))
        result = Utils.send_email(subject, body, target)
        print(result)
        self.stdout.write(self.style.SUCCESS("[+] Done!!!"))
