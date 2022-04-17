from django.db.models import QuerySet
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings


class AuthUtils:
    @staticmethod
    def user_from_token(token):
        try:
            token = {"token": token}
            data = VerifyJSONWebTokenSerializer().validate(token)
            return data["user"]
        except Exception:
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
