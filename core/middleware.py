import geoip2.database
import os
from .models import AccessLog

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOIP_PATH = os.path.join(BASE_DIR, "geoip", "GeoLite2-City.mmdb")

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.reader = geoip2.database.Reader(GEOIP_PATH)
        except FileNotFoundError:
            self.reader = None  

    def __call__(self, request):
        response = self.get_response(request)

        # Só registra acessos quando a URL é exatamente /analytics/
        if request.path == "/analytics/":
            ip = self.get_client_ip(request)
            country = "Desconhecido"

            if self.reader:
                try:
                    geo = self.reader.city(ip)
                    country = geo.country.name or "Desconhecido"
                except Exception:
                    pass

            # Se não quiser salvar "Desconhecido", pode filtrar aqui
            if country != "Desconhecido":
                AccessLog.objects.create(ip=ip, country=country)

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
