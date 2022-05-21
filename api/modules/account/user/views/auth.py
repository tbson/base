import contextlib
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from services.helpers.utils import Utils
from services.helpers.res_utils import ResUtils
from services.helpers.token_utils import TokenUtils

from modules.noti.verif.helpers.utils import VerifUtils

from modules.account.user.helpers.utils import UserUtils

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        error_message = _("Incorrect login information. Please try again")
        try:
            response = super().post(request, *args, **kwargs)
        except Exception:
            return ResUtils.err(error_message)
        if response.status_code not in range(200, 300):
            return ResUtils.err(error_message)
        refresh_token = response.data.get("refresh")
        token = response.data.get("access")
        user = TokenUtils.get_user_from_token(token)
        response = ResUtils.jwt_response_handler(token, refresh_token, user)
        return ResUtils.res(response)


class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        token = TokenUtils.refresh(refresh_token)
        if not token:
            error_message = _("Can not refresh token")
            return ResUtils.err(error_message)
        return ResUtils.res({"token": token})


class RefreshCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return ResUtils.res({})


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        with contextlib.suppress(Exception):
            token = TokenUtils.get_token_from_headers(request.headers, False)
            user = TokenUtils.get_user_from_token(token)
            user.refresh_token_signature = ""
            user.save()
        return ResUtils.res({})


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = self.request.data.get("username", "")

        default_response = ResUtils.res(
            {"verif_id": Utils.get_uuid(), "username": Utils.mask_username(username)}
        )

        verif_id = self.request.data.get("verif_id", "")
        otp_code = self.request.data.get("otp_code", "")
        if not verif_id or not otp_code:
            if not username or not isinstance(username, str):
                return default_response
            if not UserUtils.get_user_by_username(username):
                return default_response

            ok, result = VerifUtils.create(
                Utils.get_ip_list(request), username, Utils.get_lang_code(request)
            )
            if ok:
                return ResUtils.res(
                    {"verif_id": result, "username": Utils.mask_username(username)}
                )
            return ResUtils.err(result)

        password = self.request.data.get("password", "")
        password_confirm = self.request.data.get("password_confirm", "")
        if password != password_confirm:
            return ResUtils.err(
                {"password_confirm": _("Password and confirm password didn't match")}
            )
        verif = VerifUtils.get(verif_id, otp_code)
        if not verif:
            return ResUtils.err(_("Invalid OTP"))

        user = UserUtils.get_user_by_username(verif.target)
        if not user:
            return ResUtils.err(_("Can not reset password"))

        user.set_password(password)
        user.save()
        return ResUtils.res({})


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request):
        params = self.request.data

        user = self.get_object()

        old_password = params.get("old_password", 0)
        password = params.get("password", "")
        password_confirm = params.get("password_confirm", "")

        if password != password_confirm:
            return ResUtils.err(
                {"password_confirm": _("Password and confirm password didn't match")}
            )

        if not old_password or check_password(old_password, user.password) is False:
            return ResUtils.err({"old_password": _("Incorrect current password")})

        user.password = make_password(password)
        user.save()

        return ResUtils.res({})
