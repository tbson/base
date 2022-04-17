from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from services.helpers.token_utils import TokenUtils


class JWTAuth(JSONWebTokenAuthentication):
    def authenticate(self, request):

        token_header = request.META.get("HTTP_AUTHORIZATION", "")

        if token_header == TokenUtils.revoked_status:
            raise exceptions.AuthenticationFailed()

        if not token_header or token_header[:4] != "JWT ":
            return None

        auth_tuple = super().authenticate(request)
        if auth_tuple is None:
            raise exceptions.AuthenticationFailed()

        return auth_tuple
