from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.helpers.utils import Utils


class Command(BaseCommand):
    help = "generate_token"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            type=str,
            help="email address",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        username = options["username"]
        user = User.objects.get(username=username)
        token = Utils.generate_token(user)
        self.stdout.write(self.style.WARNING("JWT {}".format(token)))
        self.stdout.write(self.style.SUCCESS("Done!"))
