from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.db.models import Count
from django.http import JsonResponse
from .models import AccessLog
from .forms import ContactForm
from decouple import config
import requests


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def projects(request):
    return render(request, "projects.html")


# Limita envios por IP (máx. 3 por minuto)
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

            # 🔎 Validação do reCAPTCHA
            recaptcha_response = request.POST.get("g-recaptcha-response")
            recaptcha_secret = config("RECAPTCHA_PRIVATE_KEY")
            verify_url = "https://www.google.com/recaptcha/api/siteverify"
            payload = {"secret": recaptcha_secret, "response": recaptcha_response}
            resp = requests.post(verify_url, data=payload)
            result = resp.json()

            if not result.get("success"):
                messages.error(request, "❌ Falha na validação do reCAPTCHA. Tente novamente.")
                return render(request, "contact.html", {"form": form})

            # 🔎 Envio de e‑mail
            assunto = f"Novo contato do portfólio: {nome}"
            corpo = f"Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}"
            destinatario = config("EMAIL_TO")

            try:
                send_mail(
                    assunto,
                    corpo,
                    config("EMAIL_HOST_USER"),  # remetente válido
                    [destinatario],
                    fail_silently=False,
                )
                messages.success(request, "✅ E-mail enviado com sucesso!")
                form = ContactForm()
            except BadHeaderError:
                messages.error(request, "❌ Falha: cabeçalho inválido.")
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
