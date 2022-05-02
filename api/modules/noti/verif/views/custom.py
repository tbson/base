from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from services.helpers.res_utils import ResUtils
from services.helpers.utils import Utils
from ..helpers.utils import VerifUtils


class CheckView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        verif_id = self.request.data.get("verif_id", "")
        otp_code = self.request.data.get("otp_code", "")
        error_message = _("Invalid OTP")

        if not verif_id or not otp_code:
            return ResUtils.err({"detail": error_message})

        verif = VerifUtils.get(verif_id, otp_code)
        if not verif:
            return ResUtils.err({"detail": error_message})

        return ResUtils.res({"verif_id": verif_id, "otp_code": otp_code})


class ResendView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        verif_id = request.data.get("verif_id")
        ok, result = VerifUtils.create_again(
            Utils.get_ip_list(request), verif_id, Utils.get_lang_code(request)
        )

        if not ok:
            return ResUtils.err(result)

        return ResUtils.res(
            {"verif_id": verif_id, "username": Utils.mask_username(result)}
        )
