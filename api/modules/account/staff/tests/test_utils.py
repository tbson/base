from django.test import TestCase
from django.conf import settings
from ..helpers.model_utils import StaffModelUtils
from ..models import Staff

# Create your tests here.


class ParseExcelFile(TestCase):
    def setUp(self):
        self.model_utils = StaffModelUtils()

    def test_happy_case(self):
        file_path = "tests_data/kpi.2.staff.xlsx"
        with open("{}{}".format(settings.PUBLIC_ROOT, file_path), "rb") as file:
            self.model_utils.parse_excel_file(file)
            self.assertEqual(Staff.objects.count(), 2)
