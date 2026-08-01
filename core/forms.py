from django import forms


class ContactForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-group",
            "placeholder": "Seu nome"
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-group",
            "placeholder": "Seu e-mail"
        })
    )
    mensagem = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-group",
            "placeholder": "Sua mensagem"
        })
    )
