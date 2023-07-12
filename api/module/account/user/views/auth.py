import contextlib
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from service.string_service import StringService
from service.request_service import RequestService
from service.token_service import TokenService

from module.noti.verif.helper.util import VerifUtil
from module.account.user.helper.util import UserUtil

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        error_message = _("Incorrect login information. Please try again")
        try:
            response = super().post(request, *args, **kwargs)
        except Exception:  # skipcq: Catch every error when login
            return RequestService.err(error_message)
        if response.status_code not in range(200, 300):
            return RequestService.err(error_message)
        refresh_token = response.data.get("refresh")
        token = response.data.get("access")
        user = TokenService.get_user_from_token(token)
        response = RequestService.jwt_response_handler(token, refresh_token, user)
        return RequestService.res(response)


class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        token = TokenService.refresh(refresh_token)
        if not token:
            error_message = _("Can not refresh token")
            return RequestService.err(error_message)
        return RequestService.res({"token": token})


class RefreshCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return RequestService.res({})


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        with contextlib.suppress(Exception):
            token = TokenService.get_token_from_headers(request.headers, False)
            user = TokenService.get_user_from_token(token)
            user.refresh_token_signature = ""
            user.save()
        return RequestService.res({})


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = self.request.data.get("username", "")

        default_response = RequestService.res(
            {
                "verif_id": RequestService.get_uuid(),
                "username": StringService.apply_mask(username),
            }
        )

        verif_id = self.request.data.get("verif_id", "")
        otp_code = self.request.data.get("otp_code", "")
        password = self.request.data.get("password", "")
        password_confirm = self.request.data.get("password_confirm", "")
        if not verif_id or not otp_code:
            if password != password_confirm:
                return RequestService.err(
                    {
                        "password_confirm": _(
                            "Password and confirm password didn't match"
                        )
                    }
                )

            if not username or not isinstance(username, str):
                return default_response
            if not UserUtil.get_user_by_username(username):
                return default_response

            ok, result = VerifUtil.create(
                RequestService.get_ip_list(request),
                username,
                RequestService.get_lang_code(request),
            )
            if ok:
                return RequestService.res(
                    {"verif_id": result, "username": StringService.apply_mask(username)}
                )
            return RequestService.err(result)

        verif = VerifUtil.get(verif_id, otp_code)
        if not verif:
            return RequestService.err(_("Invalid OTP"))

        user = UserUtil.get_user_by_username(verif.target)
        if not user:
            return RequestService.err(_("Can not reset password"))

        user.set_password(password)
        user.save()
        return RequestService.res({})


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
            return RequestService.err(
                {"password_confirm": _("Password and confirm password didn't match")}
            )

        if not old_password or check_password(old_password, user.password) is False:
            return RequestService.err({"old_password": _("Incorrect current password")})

        user.password = make_password(password)
        user.save()

        return RequestService.res({})
