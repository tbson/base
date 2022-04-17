from django.core.management.base import BaseCommand
from utils.log import Log


class Command(BaseCommand):
    help = "cmd_log_ensure_db"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        Log.connect()
        Log.ensure_db()
        self.stdout.write(self.style.SUCCESS("Done!!!"))
