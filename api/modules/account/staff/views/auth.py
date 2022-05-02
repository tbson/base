from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from services.helpers.utils import Utils
from services.helpers.res_utils import ResUtils
from ..helpers.srs import StaffSr


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        return self.request.user

    def get(self, request, format=None):
        staff = self.get_user().staff
        data = StaffSr(staff).data
        return ResUtils.res(data)

    def put(self, request, format=None):
        user = self.get_user()
        staff = user.staff
        data = {}
        phone_number = request.data.get("phone_number", None)
        if phone_number:
            data = dict(phone_number=Utils.phone_to_canonical_format(phone_number))
        serializer = StaffSr(staff, partial=True, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = serializer.data
        return ResUtils.res(resp)
