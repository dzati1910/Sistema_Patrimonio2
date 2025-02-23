from msilib.schema import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic import *
from rest_framework import viewsets
from .forms import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Código da API RESTful

class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Property (API RESTful).
    Permite a criação, leitura, atualização e exclusão de bens.
    Inclui lógica personalizada para registrar movimentações ao alterar o departamento.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        Lógica personalizada para atualização de propriedades.
        Registra uma movimentação se o departamento for alterado.
        """
        old_department = self.get_object().department
        new_department = serializer.validated_data.get("department")
        if old_department != new_department:
            instance = serializer.save()
            instance.log_movement(new_department)
        else:
            serializer.save()


class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Contract (API RESTful).
    Permite a criação, leitura, atualização e exclusão de contratos.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Department (API RESTful).
    Permite a criação, leitura, atualização e exclusão de departamentos.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Category (API RESTful).
    Permite a criação, leitura, atualização e exclusão de categorias.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Código Web

@require_GET
@login_required
def list_contracts(request):
    """
    View para listar todos os contratos.
    Acesso restrito a usuários autenticados.
    """
    contracts = Contract.objects.all()
    return render(request, 'list-contracts.html', {'contracts': contracts})


class ContractCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar um novo contrato.
    Acesso restrito a usuários autenticados.
    """
    raise_exception = True
    model = Contract
    form_class = ContractForm
    template_name = 'modals/create_contracts.html'
    success_url = reverse_lazy('list-contracts')


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar um contrato existente.
    Acesso restrito a usuários autenticados.
    """
    raise_exception = True
    model = Contract
    form_class = ContractForm
    template_name = 'modals/create_contracts.html'
    success_url = reverse_lazy('list-contracts')


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class ContractDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir um contrato existente.
    Acesso restrito a usuários autenticados.
    """
    raise_exception = True
    model = Contract
    template_name = 'modals/contract_confirm_delete.html'
    success_url = reverse_lazy('list-contracts')


@require_http_methods(["GET"])
@login_required
def list_category(request):
    """
    View para listar todas as categorias.
    Acesso restrito a usuários autenticados.
    """
    categories = Category.objects.all()
    return render(request, 'list-category.html', {'categories': categories})


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova categoria.
    Acesso restrito a usuários autenticados.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'modals/create_category.html'
    success_url = reverse_lazy('list-category')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma categoria existente.
    Acesso restrito a usuários autenticados.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'modals/create_category.html'
    success_url = reverse_lazy('list-category')


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma categoria existente.
    Acesso restrito a usuários autenticados.
    """
    model = Category
    template_name = 'modals/category_confirm_delete.html'
    success_url = reverse_lazy('list-category')


@require_GET
@login_required
def list_department(request):
    """
    View para listar todos os departamentos.
    Acesso restrito a usuários autenticados.
    """
    departments = Department.objects.all()
    return render(request, 'list-department.html', {'departments': departments})


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar um novo departamento.
    Acesso restrito a usuários autenticados.
    """
    model = Department
    form_class = DepartmentForm
    template_name = 'modals/create_department.html'
    success_url = reverse_lazy('list-department')


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar um departamento existente.
    Acesso restrito a usuários autenticados.
    """
    model = Department
    form_class = DepartmentForm
    template_name = 'modals/create_department.html'
    success_url = reverse_lazy('list-department')


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class DepartmentDeleteView(DeleteView):
    """
    View para excluir um departamento existente.
    Acesso restrito a usuários autenticados.
    """
    model = Department
    template_name = 'modals/department_confirm_delete.html'
    success_url = reverse_lazy('list-department')


@require_GET
@login_required
def index(request):
    """
    View para renderizar a página inicial do sistema.
    Lista todas as propriedades disponíveis.
    Acesso restrito a usuários autenticados.
    """
    properties = Property.objects.all()
    return render(request, 'list-property.html', {'properties': properties})


class PropertyCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova propriedade.
    Acesso restrito a usuários autenticados.
    """
    model = Property
    form_class = AdminPropertyForm
    template_name = 'modals/create_property.html'
    success_url = reverse_lazy('list-property')


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma propriedade existente.
    Acesso restrito a usuários autenticados.
    """
    model = Property
    template_name = 'modals/property_confirm_delete.html'
    success_url = reverse_lazy('list-property')


class AdminPropertyUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma propriedade existente (uso administrativo).
    Acesso restrito a usuários autenticados.
    """
    model = Property
    form_class = AdminPropertyForm
    template_name = 'modals/create_property.html'
    success_url = reverse_lazy('list-property')


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma propriedade existente (uso geral).
    Acesso restrito a usuários autenticados.
    """
    model = Property
    form_class = PropertyForm
    template_name = 'modals/update_property.html'
    success_url = reverse_lazy('list-property')