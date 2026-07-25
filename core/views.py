from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.db.models import Count
from django.http import JsonResponse
from .models import AccessLog
from .forms import ContactForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def projects(request):
    return render(request, 'projects.html')

@ratelimit(key='ip', rate='3/m', block=False) # controle de envio com ratelimit
def contact(request):
    
    if getattr(request, 'limited', False):
        messages.error(request, "❌ Você enviou muitos formulários em pouco tempo. Aguarde antes de tentar novamente.")
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

            try:
                send_mail(
                    assunto,
                    corpo,
                    email,
                    ["danilo.silva.santos.1312@outlook.com"],
                    fail_silently=False,
                )
                messages.success(request, "✅ E-mail enviado com sucesso!")
                form = ContactForm()  
            except BadHeaderError:
                messages.error(request, "❌ Falha: cabeçalho inválido.")
            except Exception:
                messages.error(request, "❌ Falha ao enviar e-mail. Tente novamente.")
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