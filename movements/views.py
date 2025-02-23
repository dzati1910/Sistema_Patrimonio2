from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET, require_http_methods
from .forms import MovementForm
from .models import Movement
from .serializers import MovementSerializer


# Views do app movements

class MovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Movement (API RESTful).
    Permite a criação, leitura, atualização e exclusão de movimentações de patrimônios.
    Acesso permitido apenas para usuários autenticados ou leitura pública.
    """

    queryset = Movement.objects.all().select_related(
        'property', 'origin_department', 'destination_department'
    )
    serializer_class = MovementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filtra as movimentações com base nos parâmetros de consulta:
        - property: Filtra por ID do patrimônio.
        - origin_department: Filtra por ID do departamento de origem.
        - destination_department: Filtra por ID do departamento de destino.
        - start_date e end_date: Filtra por intervalo de datas.
        """
        queryset = super().get_queryset()
        property_id = self.request.query_params.get('property')
        origin_id = self.request.query_params.get('origin_department')
        destination_id = self.request.query_params.get('destination_department')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Filtra por propriedade, origem, destino e período
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        if origin_id:
            queryset = queryset.filter(origin_department_id=origin_id)
        if destination_id:
            queryset = queryset.filter(destination_department_id=destination_id)
        if start_date or end_date:
            start = start_date if start_date else '1900-01-01'
            end = end_date if end_date else '9999-12-31'
            queryset = queryset.filter(timestamp__range=[start, end])

        return queryset


@require_GET
@login_required
def list_movement(request):
    """
    View para listar todas as movimentações.
    Acesso restrito a usuários autenticados.
    """
    movements = Movement.objects.all()
    return render(request, 'list-movement.html', {'movements': movements})


class MovementCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova movimentação.
    Acesso restrito a usuários autenticados.
    """
    model = Movement
    form_class = MovementForm
    template_name = 'modals/create_movement.html'
    success_url = reverse_lazy('list-movement')


class MovementUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar uma movimentação existente.
    Acesso restrito a usuários autenticados.
    """
    model = Movement
    form_class = MovementForm
    template_name = 'modals/create_movement.html'
    success_url = reverse_lazy('list-movement')

    def form_valid(self, form):
        """
        Mantém os valores originais dos campos desabilitados (property e origin_department)
        durante a atualização.
        """
        form.instance.property = self.get_object().property
        form.instance.origin_department = self.get_object().origin_department
        return super().form_valid(form)


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class MovementDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma movimentação existente.
    Acesso restrito a usuários autenticados.
    """
    model = Movement
    template_name = 'modals/movement-confirm-delete.html'
    success_url = reverse_lazy('list-movement')