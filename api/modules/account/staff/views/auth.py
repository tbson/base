from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext as _
from django.db import transaction
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import ObtainJSONWebToken

from services.helpers.utils import Utils
from services.helpers.res_utils import ResUtils
from services.helpers.auth_utils import AuthUtils
from services.helpers.token_utils import TokenUtils

from modules.noti.verif.helpers.model_utils import VerifModelUtils

from ..models import Staff
from ..helpers.srs import StaffSr
from ..helpers.model_utils import StaffModelUtils


class LoginView(ObtainJSONWebToken):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        error_message = _("Incorrect login information. Please try again")
        username = request.data["username"]
        request.data["username"] = username.lower()
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return response

        new_user, new_token = TokenUtils.generate_from_username(username)
        if new_token:
            response = ResUtils.jwt_response_handler(new_token, new_user, request)
            return ResUtils.res(response)

        return ResUtils.err(error_message)


class RefreshView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token_context = TokenUtils.get_token_context(request)
        token = TokenUtils.get_token_from_header(request, False)
        token_signature = TokenUtils.get_token_signature(token)
        success, result = TokenUtils.refresh(Staff, token_context, token_signature)
        if not success:
            return ResUtils.err(result)
        return ResUtils.res({"token": result})


class RefreshCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return ResUtils.res({})


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token = TokenUtils.get_token_from_header(request, False)
        token_context = TokenUtils.get_token_context(request)
        token_signature = TokenUtils.get_token_signature(token)

        TokenUtils.revoke(Staff, token_context, token_signature)
        return ResUtils.res({})


class SignupView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        verif_id = request.data.get("verif_id", "")
        otp_code = request.data.get("otp_code", "")

        sr = StaffSr(data=request.data)
        sr.is_valid(raise_exception=True)

        data = sr.validated_data
        username = data.get("email")

        try:
            model_utils = StaffModelUtils()
            model_utils.get(username)
            exist_message = _("This email already exists in the system")
            return ResUtils.err({"detail": exist_message})
        except Staff.DoesNotExist:
            pass

        verif_model_utils = VerifModelUtils()
        if not verif_id or not otp_code:
            ok, result = verif_model_utils.create(
                Utils.get_ip_list(request), username, Utils.get_lang_code(request)
            )

            if not ok:
                return ResUtils.err(result)

            return ResUtils.res(
                {"verif_id": result, "username": Utils.mask_username(username)}
            )

        verif = verif_model_utils.get(verif_id, otp_code)
        if not verif:
            return ResUtils.err({"detail": _("Invalid OTP")})

        sr.is_valid(raise_exception=True)
        customer = sr.save()
        customer.user.password = make_password(request.data.get("password"))
        customer.user.save()
        data["token"] = AuthUtils.token_from_user(customer.user)
        return ResUtils.res(data)


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

        phone_number = request.data.get("phone_number", None)
        data = dict(phone_number=Utils.phone_to_canonical_format(phone_number))
        serializer = StaffSr(staff, partial=True, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = serializer.data
        return ResUtils.res(resp)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = self.request.data.get("username", "")

        default_response = ResUtils.res(
            {"verif_id": Utils.get_uuid(), "username": Utils.mask_username(username)}
        )

        verif_id = self.request.data.get("verif_id", "")
        otp_code = self.request.data.get("otp_code", "")

        verif_model_utils = VerifModelUtils()
        if not verif_id or not otp_code:
            if not username or not isinstance(username, str):
                return default_response

            try:
                model_utils = StaffModelUtils()
                model_utils.get(username)
            except Staff.DoesNotExist:
                return default_response

            ok, result = verif_model_utils.create(
                Utils.get_ip_list(request), username, Utils.get_lang_code(request)
            )
            if ok:
                return ResUtils.res(
                    {"verif_id": result, "username": Utils.mask_username(username)}
                )
            return ResUtils.err({"detail": result})

        password = self.request.data.get("password", "")
        password_confirm = self.request.data.get("password_confirm", "")
        if password != password_confirm:
            return ResUtils.err(
                {
                    "password_confirm": "Mật khẩu mới và mật khẩu nhập lại không trùng nhau"
                }
            )
        verif = verif_model_utils.get(verif_id, otp_code)
        if not verif:
            return ResUtils.err({"detail": _("Invalid OTP")})

        try:
            model_utils = StaffModelUtils()
            staff = model_utils.get(verif.target)
        except Staff.DoesNotExist:
            return ResUtils.err({"detail": _("Can not reset password")})

        user = staff.user
        user.set_password(password)
        user.save()
        return ResUtils.res({})


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request, format=None):
        if settings.STAFF_NO_EMAIL_FIX_PASSWORD:
            return ResUtils.res({})

        params = self.request.data

        user = self.get_object()

        old_password = params.get("old_password", 0)
        password = params.get("password", "")
        password_confirm = params.get("password_confirm", "")

        if password != password_confirm:
            return ResUtils.err(
                {
                    "password_confirm": "Mật khẩu mới và mật khẩu nhập lại không trùng nhau"
                }
            )

        if not old_password or check_password(old_password, user.password) is False:
            return ResUtils.err({"old_password": _("Incorrect current password")})

        user.password = make_password(password)
        user.save()

        return ResUtils.res({})
