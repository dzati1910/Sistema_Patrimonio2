from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .forms import *
from .models import User, SalesData
from .serializers import UserSerializer
from django.contrib.auth import *
from django.shortcuts import render, redirect


# Views do app core

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo User (API RESTful).
    Permite a criação, leitura, atualização e exclusão de usuários.
    Acesso restrito a administradores.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


def rend_index(request):
    """
    View para renderizar a página inicial.
    """
    return render(request, 'index.html')


def dash_view(request):
    """
    View para renderizar a página do dashboard.
    """
    return render(request, 'dashboard.html')


def serve_view(request, param):
    """
    View de exemplo para servir conteúdo com base em um parâmetro.
    (Implementação pendente)
    """
    pass


class RegisterView(CreateView):
    """
    View para registro de novos usuários.
    Utiliza um formulário personalizado (CustomUserCreationForm).
    """
    form_class = CustomUserCreationForm
    template_name = 'modals/register.html'
    success_url = reverse_lazy('/core/login/')  # Redireciona para a página de login após o registro


class CustomLoginView(LoginView):
    """
    View personalizada para login de usuários.
    Utiliza um formulário personalizado (CustomAuthenticationForm).
    """
    form_class = CustomAuthenticationForm
    template_name = 'modals/login.html'
    success_url = reverse_lazy('/core/index/')


def custom_logout(request):
    """
    View para logout personalizado.
    Realiza logout do usuário e redireciona para a página inicial.
    """
    logout(request)
    return redirect('index')