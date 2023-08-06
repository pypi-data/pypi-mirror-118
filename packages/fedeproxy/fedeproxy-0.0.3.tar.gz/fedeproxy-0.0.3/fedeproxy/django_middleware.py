from django.conf import settings

from fedeproxy.domain import fedeproxy


class Fedeproxy:
    def __init__(self, get_response):
        self.get_response = get_response
        self.fedeproxy = fedeproxy.Fedeproxy(
            settings.FEDEPROXY_FORGE_FACTORY,
            settings.FEDEPROXY_FORGE_URL,
            settings.FEDEPROXY_FORGE_DIRECTORY,
        )

    def __call__(self, request):
        request.fedeproxy = self.fedeproxy
        response = self.get_response(request)
        return response
