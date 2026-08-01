# Middleware de analytics removido do sistema.
# O projeto não registra mais acessos por geolocalização.


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
