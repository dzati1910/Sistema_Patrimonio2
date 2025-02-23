from rest_framework import serializers
from .models import Maintenance


class MaintenanceSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    scheduled_date = serializers.DateField(required=True)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    description = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Maintenance
        fields = '__all__'
        read_only_fields = ['id']

    def get_is_overdue(self, obj):
        return obj.is_overdue()


