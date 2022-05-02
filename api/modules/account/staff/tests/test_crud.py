import json
from rest_framework.test import APIClient
from django.test import TestCase
from services.helpers.token_utils import TokenUtils
from ..models import Staff
from ..helpers.utils import StaffUtils

# Create your tests here.


class StaffTestCase(TestCase):
    def setUp(self):
        self.base_url = "/api/v1/account/staff/"
        self.base_url_params = "/api/v1/account/staff/{}"
        staff = StaffUtils.seeding(1, True)
        staff.user.is_staff = True
        staff.user.save()

        token = TokenUtils.generate_test_token(staff)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

        self.items = StaffUtils.seeding(3)

    def test_list(self):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(resp["count"], 3)

    def test_detail(self):
        # Item not exist
        resp = self.client.get(self.base_url_params.format(0))
        self.assertEqual(resp.status_code, 404)

        # Item exist
        resp = self.client.get(self.base_url_params.format(self.items[0].pk))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        item3 = StaffUtils.seeding(3, True, False)
        item4 = StaffUtils.seeding(4, True, False)

        # Add duplicate
        resp = self.client.post(
            self.base_url, json.dumps(item3), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

        # Add success
        resp = self.client.post(
            self.base_url, json.dumps(item4), content_type="application/json"
        )

        # self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(Staff.objects.count(), 4)

    def test_edit(self):
        item2 = StaffUtils.seeding(2, True, False)

        # Update not exist
        resp = self.client.put(
            self.base_url_params.format(0),
            json.dumps(item2),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 404)

        # Update duplicate
        resp = self.client.put(
            self.base_url_params.format(self.items[0].pk),
            json.dumps(item2),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

        # Update success
        resp = self.client.put(
            self.base_url_params.format(self.items[1].pk),
            json.dumps(item2),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        # Remove not exist
        resp = self.client.delete(self.base_url_params.format(0))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(Staff.objects.count(), 3)

        # Remove single success
        resp = self.client.delete(self.base_url_params.format(self.items[1].pk))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Staff.objects.count(), 2)

        # Remove list success
        resp = self.client.delete(
            self.base_url
            + "?ids={}".format(",".join([str(self.items[0].pk), str(self.items[2].pk)]))
        )
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Staff.objects.count(), 0)
