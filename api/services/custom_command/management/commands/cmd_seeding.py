from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import Group
from modules.kpi.quota_template.helpers.model_utils import QuotaTemplateModelUtils
from modules.account.staff.helpers.srs import StaffSr
from modules.account.staff.consts import StaffType


class Command(BaseCommand):
    help = "cmd_seeding"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quota_template_mu = QuotaTemplateModelUtils()

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))

        self.seeding_quota_template()
        self.seeding_groups()
        self.seeding_users()
        self.seeding_campaign()
        self.seeding_quotas()
        self.seeding_quota_values()

        self.stdout.write(self.style.SUCCESS("Done..."))

    def seeding_quota_template(self):
        file_path = "tests_data/quota-template.xlsx"
        with open("{}{}".format(settings.PUBLIC_ROOT, file_path), "rb") as file:
            self.quota_template_mu.parse_excel_file(file)

    def seeding_groups(self):
        Group.objects.create(name="Admin")

    def seeding_users(self):
        for i in range(5):
            data = dict(
                uid=f"staff{i}",
                email=f"staff{i}@localhost",
                phone_number=f"+8490669652{i}",
                first_name=f"First {i}",
                last_name=f"Last {i}",
                groups=Group.objects.all().values_list("id", flat=True),
                type=StaffType.OFFICIAL,
            )
            serializer = StaffSr(data=data)
            serializer.is_valid(raise_exception=True)
            print(f"[+] Creating {data['email']}")
            serializer.save()

    def seeding_campaign(self):
        pass

    def seeding_quotas(self):
        pass

    def seeding_quota_values(self):
        pass
