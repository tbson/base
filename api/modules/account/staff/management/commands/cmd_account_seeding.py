from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from modules.configuration.variable.helpers.model_utils import VariableModelUtils
from modules.account.staff.helpers.srs import StaffSr


class Command(BaseCommand):
    help = "cmd_account_seeding"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        password = "SamplePassword123!@#"
        # Create super user
        try:
            user = User.objects.create_user(
                username="admin", email="", password=password
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
                "email": "admin@localhost",
                "phone_number": "+84906696526",
                "first_name": "Admin",
                "last_name": "Localhost",
                "groups": [staff_group.pk],
            }
        ]

        for data in staff_list:
            serializer = StaffSr(data=data)
            if serializer.is_valid(raise_exception=True):
                staff = serializer.save()
                staff.user.set_password(password)
                staff.user.save()
                if staff.user.username == "admin@localhost":
                    staff.user.is_staff = True
                    staff.user.save()

        def print_result(uid: str, value: str):
            self.stdout.write(self.style.SUCCESS(f"[+] Seeding: {uid} = {value}"))

        variable_model_utils = VariableModelUtils()
        variable_model_utils.settings_seeding(print_result)
        self.stdout.write(self.style.SUCCESS("Done!!!"))
