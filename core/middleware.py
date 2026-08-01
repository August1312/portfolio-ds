import geoip2.database
from django.conf import settings

from .models import AccessLog


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.reader = None
        try:
            self.reader = geoip2.database.Reader(settings.GEOIP_PATH)
        except FileNotFoundError:
            self.reader = None

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith(("/static/", "/media/", "/admin/")):
            return response

        ip = self.get_client_ip(request)
        if not ip:
            return response

        country = "Desconhecido"
        state = "Desconhecido"
        city = "Desconhecido"

        if self.reader:
            try:
                geo = self.reader.city(ip)
                country = geo.country.name or "Desconhecido"
                state = geo.subdivisions.most_specific.name or "Desconhecido"
                city = geo.city.name or "Desconhecido"
            except Exception:
                pass

        AccessLog.objects.create(
            ip=ip,
            country=country,
            state=state,
            city=city,
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ips = [ip.strip() for ip in x_forwarded_for.split(",") if ip.strip()]
            if ips:
                return ips[0]
        return request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_REAL_IP")
