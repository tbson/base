from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from services.helpers.utils import Utils
from services.helpers.res_utils import ResUtils
from ..helpers.srs import StaffSr
from ..helpers.utils import StaffUtils


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        return self.request.user

    def get(self, request):
        staff = self.get_user().staff
        data = StaffSr(staff).data
        return ResUtils.res(data)

    def put(self, request):
        user = self.get_user()
        staff = user.staff
        data = {}
        if phone_number := request.data.get("phone_number", None):
            data = dict(phone_number=Utils.phone_to_canonical_format(phone_number))
        staff = StaffUtils.update_staff(staff, data)
        sr = StaffSr(staff)
        return ResUtils.res(sr.data)
