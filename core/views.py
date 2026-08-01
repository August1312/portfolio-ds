import os

import requests
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm
from .models import AccessLog


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def projects(request):
    return render(request, "projects.html")


@ratelimit(key="ip", rate="3/m", block=False)
def contact(request):

    if getattr(request, "limited", False):
        messages.error(
            request,
            "❌ Você enviou muitos formulários em pouco tempo. Aguarde antes de tentar novamente.",
        )
        form = ContactForm()
        return render(request, "contact.html", {"form": form})

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            mensagem = form.cleaned_data["mensagem"]

            assunto = f"Novo contato do portfólio: {nome}"
            corpo = f"Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}"
            destinatario = (os.environ.get("EMAIL_TO") or "").strip()
            remetente = (os.environ.get("DEFAULT_FROM_EMAIL") or os.environ.get("EMAIL_HOST_USER") or "").strip()
            smtp_user = (os.environ.get("EMAIL_HOST_USER") or "").strip()
            smtp_password = (os.environ.get("EMAIL_HOST_PASSWORD") or "").strip()

            if not destinatario or not remetente or not smtp_user or not smtp_password:
                messages.error(
                    request,
                    "❌ O envio de e-mail não está configurado no Render. Verifique EMAIL_TO, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER e EMAIL_HOST_PASSWORD.",
                )
                return render(request, "contact.html", {"form": form})

            try:
                send_mail(
                    assunto,
                    corpo,
                    remetente,
                    [destinatario],
                    fail_silently=False,
                )
                messages.success(request, "✅ E-mail enviado com sucesso!")
                form = ContactForm()
            except BadHeaderError:
                messages.error(request, "❌ Falha: cabeçalho inválido.")
            except (ConnectionError, TimeoutError, OSError, ValueError) as e:
                messages.error(
                    request,
                    "❌ Não foi possível enviar o e-mail neste momento. Verifique as variáveis SMTP do Render.",
                )
            except Exception as e:
                messages.error(request, f"❌ Falha ao enviar e-mail: {str(e)}")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def analytics(request):
    data = (
        AccessLog.objects.values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return render(request, "analytics.html", {"data": data})


def analytics_data(request):
    data = (
        AccessLog.objects.values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return JsonResponse(list(data), safe=False)
