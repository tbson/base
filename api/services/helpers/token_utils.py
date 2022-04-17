import hashlib
from django.db.models import QuerySet
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from services.helpers.model_utils import ModelUtils
from services.helpers.utils import Utils


class TokenUtils:
    revoked_status = "REVOKED"

    @staticmethod
    def get_test_fp() -> str:
        return "395fb184305a022fe98eab14c8328d21"

    @staticmethod
    def get_test_user_agent() -> str:
        return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15"

    @staticmethod
    def get_token_from_header(request, is_jwt=True):
        prefix = "JWT "
        if not is_jwt:
            prefix = "bearer "

        token_header = request.META.get("HTTP_AUTHORIZATION")

        if not token_header:
            return ""

        if not token_header.startswith(prefix):
            return ""

        return token_header.split(prefix)[-1]

    @staticmethod
    def get_token_context(request) -> str:
        if settings.TESTING:
            fp = TokenUtils.get_test_fp()
            user_agent = TokenUtils.get_test_user_agent()
        else:
            fp = request.META.get("HTTP_FINGERPRINT", "")
            user_agent = str(request.META["HTTP_USER_AGENT"])
        return "{}{}".format(fp, hashlib.md5(user_agent.encode("utf-8")).hexdigest())

    @staticmethod
    def get_token_signature(token: str) -> str:
        return token.split(".")[-1]

    @staticmethod
    def parse(token: str) -> QuerySet:
        try:
            return (
                VerifyJSONWebTokenSerializer()
                .validate({"token": token})
                .get("user", None)
            )
        except Exception:
            return None

    @staticmethod
    def generate_test_token(extended_user: QuerySet) -> str:
        token = TokenUtils.generate(extended_user.user)
        token_context = TokenUtils.get_token_context({})
        token_signature = TokenUtils.get_token_signature(token)
        TokenUtils.update_token_meta_data(extended_user, token_context, token_signature)
        return token

    @staticmethod
    def generate(user: QuerySet) -> str:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    @staticmethod
    def revoke(model: QuerySet, token_context: str, token_signature) -> bool:
        extended_user = ModelUtils.get(model)(
            token_context=token_context, token_signature=token_signature
        )

        if not extended_user:
            return False

        extended_user.token_signature = ""
        extended_user.save()
        return True

    @staticmethod
    def is_revoked(model: QuerySet, token_context: str, token_signature: str) -> bool:
        if not token_context or not token_signature:
            return True

        extended_user = ModelUtils.get(model)(
            token_context=token_context, token_signature=token_signature
        )
        return not bool(extended_user)

    @staticmethod
    def update_token_meta_data(
        extended_user: QuerySet, token_context: str, token_signature: str
    ):
        extended_user.token_context = token_context
        extended_user.token_signature = token_signature
        extended_user.token_refresh_limit = Utils.shift_from_now(
            "minutes", settings.JWT_REFRESH_EXPIRATION_DELTA
        )
        extended_user.save()

    @staticmethod
    def refresh(model: QuerySet, token_context: str, token_signature: str) -> str:
        extended_user = ModelUtils.get(model)(
            token_context=token_context, token_signature=token_signature
        )

        if not extended_user:
            return (False, "No extended user")

        if extended_user.token_refresh_limit < Utils.now():
            return (False, "Invalid refresh limit")

        token = TokenUtils.generate(extended_user.user)
        token_signature = TokenUtils.get_token_signature(token)

        TokenUtils.update_token_meta_data(extended_user, token_context, token_signature)

        return (True, token)

    @staticmethod
    def generate_from_username(username: str):
        try:
            user = User.objects.get(username=username)
            return user, TokenUtils.generate(user)
        except Exception:
            return None, ""
