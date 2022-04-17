from rest_framework.permissions import AllowAny
from services.helpers.token_utils import TokenUtils
from modules.account.staff.models import Staff


class StripJWT:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        token_header = request.META.get("HTTP_AUTHORIZATION")
        if token_header:
            token = TokenUtils.get_token_from_header(request)
            bearer_token = "bearer {}".format(token)

            token_context = TokenUtils.get_token_context(request)
            token_signature = TokenUtils.get_token_signature(token)

            if token and TokenUtils.is_revoked(Staff, token_context, token_signature):
                request.META["HTTP_AUTHORIZATION"] = TokenUtils.revoked_status

            try:
                if AllowAny in view_func.view_class.permission_classes and token:
                    request.META["HTTP_AUTHORIZATION"] = bearer_token
            except AttributeError:
                pass
