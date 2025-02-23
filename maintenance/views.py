from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET, require_http_methods
from .forms import *
from .models import Maintenance
from .serializers import MaintenanceSerializer


# Views do app maintenance

class MaintenanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Maintenance (API RESTful).
    Permite a criação, leitura, atualização e exclusão de registros de manutenção.
    Acesso permitido apenas para usuários autenticados ou leitura pública.
    """
    queryset = Maintenance.objects.all().select_related('property')
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filtra manutenções por status (pendentes, concluídas, atrasadas)
        usando parâmetros de consulta na URL.
        """
        queryset = super().get_queryset()
        overdue = self.request.query_params.get('overdue')

        if overdue:
            today = timezone.now().date()
            return queryset.filter(scheduled_date__lt=today, completion_date__isnull=True)
        return queryset


class MaintenanceListView(LoginRequiredMixin, ListView):
    """
    View para listar todas as manutenções.
    Acesso restrito a usuários autenticados.
    """
    model = Maintenance
    template_name = 'list-maintenance.html'
    context_object_name = 'maintenance'

    @method_decorator(require_GET)
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        """
        Verifica a autenticação do usuário antes de processar a view.
        """
        return super().dispatch(*args, **kwargs)


class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova manutenção.
    Acesso restrito a usuários autenticados.
    """
    model = Maintenance
    form_class = AdminMaintenanceForm
    template_name = 'modals/create_maintenance.html'
    success_url = reverse_lazy('list-maintenance')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        """
        Verifica a autenticação do usuário antes de processar a view.
        """
        return super().dispatch(*args, **kwargs)


class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma manutenção existente.
    Acesso restrito a usuários autenticados.
    """
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'modals/create_maintenance.html'
    success_url = reverse_lazy('list-maintenance')


class AdminMaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma manutenção existente (uso administrativo).
    Acesso restrito a usuários autenticados.
    """
    model = Maintenance
    form_class = AdminMaintenanceForm
    template_name = 'modals/create_maintenance.html'
    success_url = reverse_lazy('list-maintenance')

    def get_form_kwargs(self):
        """
        Garante que os campos desabilitados (property e scheduled_date)
        sejam repassados ao formulário durante a atualização.
        """
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            data = kwargs['data'].copy()
            data['property'] = self.object.property_id
            data['scheduled_date'] = self.object.scheduled_date
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        """
        Lógica para definir a data de conclusão automaticamente
        quando o status é alterado para 'Completado'.
        """
        if form.cleaned_data['status'] == 'Completado' and not form.cleaned_data.get('completion_date'):
            form.instance.completion_date = timezone.localdate()
        return super().form_valid(form)


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma manutenção existente.
    Acesso restrito a usuários autenticados.
    """
    model = Maintenance
    template_name = 'modals/maintenance-confirm-delete.html'
    success_url = reverse_lazy('list-maintenance')