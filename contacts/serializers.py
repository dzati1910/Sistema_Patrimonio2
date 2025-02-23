from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    active_contracts = serializers.SerializerMethodField()  # Campo personalizado para contagens

    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'tax_id',
            'contact',
            'active_contracts'
        ]
        read_only_fields = ['id']

    def get_active_contracts(self, obj):
        """
        Calcula a quantidade de contratos ativos para o fornecedor
        """
        from django.utils import timezone  # Evita circular imports
        today = timezone.now().date()
        return obj.contract_set.filter(
            start_date__lte=today,
            end_date__gte=today
        ).count()