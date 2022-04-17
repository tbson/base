from django.core.management.base import BaseCommand
from modules.configuration.variable.helpers.model_utils import VariableModelUtils


class Command(BaseCommand):
    help = "cmd_variable_seeding"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))

        variable_model_utils = VariableModelUtils()

        def print_result(uid: str, value: str):
            self.stdout.write(self.style.SUCCESS(f"[+] Seeding: {uid} = {value}"))

        variable_model_utils.settings_seeding(print_result)

        self.stdout.write(self.style.SUCCESS("Done!!!"))
