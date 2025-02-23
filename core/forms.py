from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário personalizado para criação de usuários.
    Estende o UserCreationForm do Django para incluir o campo de CPF (tax_id).
    """

    tax_id = forms.CharField(
        max_length=11,
        required=False,
        label="CPF",
        help_text="Opcional. Insira o CPF do usuário."
    )

    class Meta:
        model = User
        fields = ("username", "tax_id", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Salva o usuário no banco de dados.
        Se commit=True, o usuário é salvo imediatamente.
        Retorna o usuário criado.
        """
        user = super().save(commit=False)
        user.tax_id = self.cleaned_data["tax_id"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulário personalizado para autenticação de usuários.
    Personaliza as mensagens de erro para melhorar a experiência do usuário.
    """

    error_messages = {
        'invalid_login': "Credenciais inválidas. Por favor, tente novamente.",
        'inactive': "Esta conta está inativa.",
    }