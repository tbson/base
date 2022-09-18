from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from service.format_service import FormatService
from service.request_service import RequestService
from module.account.staff.helper.sr import StaffSr
from module.account.staff.helper.util import StaffUtil


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        return self.request.user

    def get(self, request):
        staff = self.get_user().staff
        data = StaffSr(staff).data
        return RequestService.res(data)

    def put(self, request):
        user = self.get_user()
        staff = user.staff
        data = {}
        if phone_number := request.data.get("phone_number", None):
            data = dict(
                phone_number=FormatService.phone_to_canonical_format(phone_number)
            )
        staff = StaffUtil.update_staff(staff, data)
        sr = StaffSr(staff)
        return RequestService.res(sr.data)
