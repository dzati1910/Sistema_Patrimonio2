from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import *
from rest_framework import viewsets

from .forms import SupplierForm
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Supplier (API RESTful).
    Permite a criação, leitura, atualização e exclusão de fornecedores.
    Acesso permitido apenas para usuários autenticados ou leitura pública.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Views do app contacts

@require_GET
@login_required
@user_passes_test(lambda u: u.is_authenticated)
def list_contacts(request):
    """
    View para listar todos os fornecedores.
    Acesso restrito a usuários autenticados.
    """
    contacts = Supplier.objects.all()
    return render(request, 'list-contacts.html', {'contacts': contacts})


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar um novo fornecedor.
    Acesso restrito a usuários autenticados.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'modals/create_supplier.html'
    success_url = reverse_lazy('list-contacts')  # Redireciona para a lista de fornecedores

    def form_valid(self, form):
        """
        Executa ações adicionais após a validação do formulário.
        """
        response = super().form_valid(form)
        return response

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Verifica a autenticação do usuário antes de processar a view.
        """
        return super().dispatch(*args, **kwargs)


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar um fornecedor existente.
    Acesso restrito a usuários autenticados.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'modals/create_supplier.html'
    success_url = reverse_lazy('list-contacts')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Verifica a autenticação do usuário antes de processar a view.
        """
        return super().dispatch(*args, **kwargs)


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir um fornecedor existente.
    Acesso restrito a usuários autenticados.
    """
    model = Supplier
    template_name = 'modals/supplier-confirm-delete.html'
    success_url = reverse_lazy('list-contacts')