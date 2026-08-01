from django import forms


class ContactForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-field",
            "placeholder": "Seu nome"
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-field",
            "placeholder": "Seu e-mail"
        })
    )
    mensagem = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-field form-field-textarea",
            "placeholder": "Sua mensagem"
        })
    )
