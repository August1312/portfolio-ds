import os

import requests
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm
from .models import AccessLog


def send_contact_via_resend(subject, body, recipient_email, sender_email):
    api_key = (os.environ.get("RESEND_API_KEY") or getattr(settings, "RESEND_API_KEY", "") or "").strip()
    if not api_key:
        raise ValueError("RESEND_API_KEY não configurada.")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": sender_email,
            "to": [recipient_email],
            "subject": subject,
            "text": body,
        },
        timeout=20,
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Erro Resend: {response.status_code} - {response.text}")

    return response


def get_country_analytics_data():
    return (
        AccessLog.objects.values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


@require_GET
def home(request):
    return render(request, "home.html")


@require_GET
def about(request):
    return render(request, "about.html")


@require_GET
def projects(request):
    return render(request, "projects.html")


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="3/m", block=False)
def contact(request):
    if getattr(request, "limited", False):
        messages.error(
            request,
            "❌ Você enviou muitos formulários em pouco tempo. Aguarde antes de tentar novamente.",
        )
        return render(request, "contact.html", {"form": ContactForm()})

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            mensagem = form.cleaned_data["mensagem"]

            assunto = f"Novo contato do portfólio: {nome}"
            corpo = f"Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}"
            destinatario = (os.environ.get("EMAIL_TO") or "").strip()
            remetente = (os.environ.get("DEFAULT_FROM_EMAIL") or "noreply@localhost").strip()
            api_key = (os.environ.get("RESEND_API_KEY") or getattr(settings, "RESEND_API_KEY", "") or "").strip()

            if not destinatario or not remetente or not api_key:
                messages.error(
                    request,
                    "❌ O envio de e-mail não está configurado no Render. Verifique EMAIL_TO, DEFAULT_FROM_EMAIL e RESEND_API_KEY.",
                )
                return render(request, "contact.html", {"form": form})

            try:
                send_contact_via_resend(
                    assunto,
                    corpo,
                    destinatario,
                    remetente,
                )
                messages.success(request, "✅ E-mail enviado com sucesso!")
                form = ContactForm()
            except (requests.RequestException, RuntimeError, ValueError) as exc:
                messages.error(request, f"❌ Não foi possível enviar o e-mail: {exc}")
            except Exception as exc:
                messages.error(request, f"❌ Falha ao enviar e-mail: {str(exc)}")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


@require_GET
def analytics(request):
    return render(request, "analytics.html", {"data": get_country_analytics_data()})


@require_GET
def analytics_data(request):
    return JsonResponse(list(get_country_analytics_data()), safe=False)
