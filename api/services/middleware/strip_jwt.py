from rest_framework.permissions import AllowAny
from services.helpers.token_utils import TokenUtils


class StripJWT:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        token_header = request.headers.get("Authorization")
        if token_header:
            token = TokenUtils.get_token_from_headers(request.headers)
            bearer_token = "bearer {}".format(token)

            try:
                if AllowAny in view_func.view_class.permission_classes and token:
                    request.META["HTTP_AUTHORIZATION"] = bearer_token
            except AttributeError:
                pass
