from django.core.management.base import BaseCommand
from modules.configuration.variable.helpers.utils import VariableUtils


class Command(BaseCommand):
    help = "cmd_variable_seeding"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))

        def print_result(uid: str, value: str):
            self.stdout.write(self.style.SUCCESS(f"[+] Seeding: {uid} = {value}"))

        VariableUtils.settings_seeding(print_result)

        self.stdout.write(self.style.SUCCESS("Done!!!"))
