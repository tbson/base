from services.helpers.kpi_config import KPIConfig


class Cors:
    def __init__(self, get_response):
        KPIConfig.load()
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        return response
