import json
from rest_framework.test import APIClient
from django.test import TestCase
from services.helpers.utils import Utils
from modules.account.staff.helpers.utils import StaffUtils
from modules.noti.verif.helpers.utils import VerifUtils


class StaffTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anonClient = APIClient()
        self.base_url = "/api/v1/account/user/"
        self.profile_base_url = "/api/v1/account/staff/profile/"

    def test_reset_password(self):
        staff = StaffUtils.seeding(1, True)
        data = {
            "username": staff.user.username,
        }

        # Step 1 -> request OTP
        resp = self.client.post(
            f"{self.base_url}reset-password/",
            json.dumps(data),
            content_type="application/json",
        )

        status_code = resp.status_code
        resp = resp.json()
        verif_id = resp["verif_id"]
        self.assertEqual(status_code, 200)
        self.assertTrue("verif_id" in resp)
        self.assertTrue("username" in resp)

        # Step 2 -> check OTP
        otp_payload = {
            "verif_id": verif_id,
            "otp_code": VerifUtils.get_default_otp(),
        }
        resp = self.client.post(
            "/api/v1/noti/verif/check/",
            json.dumps(otp_payload),
            content_type="application/json",
        )
        status_code = resp.status_code
        self.assertEqual(status_code, 200)

        # Step 3 -> verify
        password_payload = {"password": "Qwerty!@#4567890"}
        payload = password_payload | otp_payload

        resp = self.client.post(
            f"{self.base_url}reset-password/",
            json.dumps(payload),
            content_type="application/json",
        )

        status_code = resp.status_code
        resp = resp.json()
        self.assertEqual(status_code, 200)
        self.assertEqual(resp, {})

        # Step 4 -> login
        resp = self.client.post(
            f"{self.base_url}login/",
            json.dumps(
                {
                    "username": staff.user.username,
                    "password": password_payload["password"],
                }
            ),
            content_type="application/json",
        )

        status_code = resp.status_code
        self.assertEqual(status_code, 200)
        resp = resp.json()
        self.assertTrue("token" in resp)

    def test_change_password(self):
        staff = StaffUtils.seeding(1, True)
        self.client.force_authenticate(user=staff.user)

        data = {
            "old_password": "Qwerty!@#456",
            "password": "Qwerty!@#456789",
        }

        wrong_data = {
            "old_password": "password",
            "password": "Qwerty!@#456789",
        }

        # Step 0 -> wrong password
        resp = self.client.post(
            f"{self.base_url}change-password/",
            json.dumps(wrong_data),
            content_type="application/json",
        )

        status_code = resp.status_code
        self.assertEqual(status_code, 400)
        resp = resp.json()
        self.assertEqual(
            resp["password_confirm"], "Password and confirm password didn't match"
        )

        # Step 1 -> change
        resp = self.client.post(
            f"{self.base_url}change-password/",
            json.dumps(data),
            content_type="application/json",
        )

        status_code = resp.status_code
        self.assertEqual(status_code, 200)
        resp = resp.json()
        self.assertEqual(resp, {})

        # Step 2 -> login
        resp = self.client.post(
            f"{self.base_url}login/",
            json.dumps({"username": staff.user.username, "password": data["password"]}),
            content_type="application/json",
        )

        status_code = resp.status_code
        self.assertEqual(status_code, 200)
        resp = resp.json()
        self.assertTrue("token" in resp)

    def test_view_profile(self):
        staff_data = StaffUtils.seeding(1, True, False)
        staff = StaffUtils.seeding(1, True)

        # Before authenticate
        resp = self.anonClient.get(self.profile_base_url)
        self.assertEqual(resp.status_code, 401)

        # After authenticate
        self.client.force_authenticate(user=staff.user)
        resp = self.client.get(self.profile_base_url)

        status_code = resp.status_code
        self.assertEqual(status_code, 200)
        resp = resp.json()
        self.assertEqual(resp["email"], staff_data["email"])

    def test_update_profile(self):
        staff = StaffUtils.seeding(1, True)

        data = {"phone_number": "0906696555"}

        # Before authenticate
        resp = self.anonClient.put(
            self.profile_base_url,
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 401)

        # After authenticate
        self.client.force_authenticate(user=staff.user)
        resp = self.client.put(
            self.profile_base_url,
            json.dumps(data),
            content_type="application/json",
        )

        status_code = resp.status_code
        resp = resp.json()
        self.assertEqual(status_code, 200)
        self.assertEqual(
            resp["phone_number"], Utils.phone_to_canonical_format(data["phone_number"])
        )
