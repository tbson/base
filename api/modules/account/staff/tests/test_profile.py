import json
from rest_framework.test import APIClient
from django.test import TestCase
from services.helpers.utils import Utils
from modules.account.staff.helpers.utils import StaffUtils


class StaffProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anonClient = APIClient()
        self.base_url = "/api/v1/account/staff/profile/"

    def test_view_profile(self):
        staff_data = StaffUtils.seeding(1, True, False)
        staff = StaffUtils.seeding(1, True)

        # Before authenticate
        resp = self.anonClient.get(self.base_url)
        self.assertEqual(resp.status_code, 401)

        # After authenticate
        self.client.force_authenticate(user=staff.user)
        resp = self.client.get(self.base_url)

        status_code = resp.status_code
        self.assertEqual(status_code, 200)
        resp = resp.json()
        self.assertEqual(resp["email"], staff_data["email"])

    def test_update_profile(self):
        staff = StaffUtils.seeding(1, True)

        data = {"phone_number": "0906696555"}

        # Before authenticate
        resp = self.anonClient.put(
            self.base_url,
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 401)

        # After authenticate
        self.client.force_authenticate(user=staff.user)
        resp = self.client.put(
            self.base_url,
            json.dumps(data),
            content_type="application/json",
        )

        status_code = resp.status_code
        resp = resp.json()
        self.assertEqual(status_code, 200)
        self.assertEqual(
            resp["phone_number"], Utils.phone_to_canonical_format(data["phone_number"])
        )
