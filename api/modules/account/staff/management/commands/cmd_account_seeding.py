from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from modules.configuration.variable.helpers.utils import VariableUtils
from modules.account.staff.helpers.utils import StaffUtils

User = get_user_model()


class Command(BaseCommand):
    help = "cmd_account_seeding"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        password = "SamplePassword123!@#"
        # Create super user
        try:
            user = User.objects.create_user(
                username="root", email="root@localhost", password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except Exception:
            pass

        # Create group
        Group.objects.get_or_create(name="Manager")
        Group.objects.get_or_create(name="Admin")
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        permissions = Permission.objects.all()
        for group in Group.objects.all():
            group.permissions.set(permissions)

        staff_list = [
            {
                "password": password,
                "email": "admin@localhost",
                "phone_number": "+84906696526",
                "first_name": "Admin",
                "last_name": "Localhost",
                "groups": [staff_group.pk],
            }
        ]

        for data in staff_list:
            staff = StaffUtils.create_staff(data)
            if staff.user.username == "admin@localhost":
                staff.user.is_staff = True
                staff.user.save()

        def print_result(uid: str, value: str):
            self.stdout.write(self.style.SUCCESS(f"[+] Seeding: {uid} = {value}"))

        VariableUtils.settings_seeding(print_result)
        self.stdout.write(self.style.SUCCESS("Done!!!"))
