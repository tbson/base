from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


class AuthUtils:
    @staticmethod
    def user_from_token(token):
        try:
            token = {"token": token}
            data = TokenVerifySerializer().validate(token)
            return data["user"]
        except Exception:  # skipcq: whatever error
            return None

    @staticmethod
    def token_from_user(user: QuerySet) -> str:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    @staticmethod
    def make_password(raw_password):
        return make_password(raw_password)

    @staticmethod
    def check_password(raw_password, hash_password):
        return check_password(raw_password, hash_password)

    @staticmethod
    def is_authenticated(username, password):
        try:
            user = User.objects.get(username=username)
            return AuthUtils.check_password(password, user.password)
        except User.DoesNotExist:
            return False
