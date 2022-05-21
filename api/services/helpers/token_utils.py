from typing import Union
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TokenUtils:
    @staticmethod
    def get_token_from_headers(headers: dict, is_jwt=True):
        prefix = "JWT " if is_jwt else "bearer "
        full_token = headers.get("Authorization")
        if not full_token:
            return ""
        token_arr = full_token.split(" ")
        if len(token_arr) != 2:
            return ""
        prefix = token_arr[0]
        token = token_arr[1]

        if not token or prefix not in ["bearer", "JWT"]:
            return ""

        return token

    @staticmethod
    def get_token_signature(token: str) -> str:
        return token.split(".")[-1]

    @staticmethod
    def refresh(refresh_token: str) -> str:
        try:
            return str(RefreshToken(refresh_token).access_token)
        except Exception:
            return ""

    @staticmethod
    def __generate(user: QuerySet) -> str:
        return str(RefreshToken.for_user(user))

    @staticmethod
    def get_token_from_username(username: str) -> str:
        try:
            user = User.objects.get(username=username)
            return TokenUtils.__generate(user)
        except Exception:
            return ""

    @staticmethod
    def get_user_from_token(token: str) -> Union[QuerySet, None]:
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        except Exception as e:
            print(repr(e))
            return None
