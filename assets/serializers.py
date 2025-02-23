from rest_framework import serializers
from .models import Property, Category, Department, Contract
from contacts.serializers import SupplierSerializer
from maintenance.serializers import MaintenanceSerializer
from movements.serializers import MovementSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        # Valida o formato do RFID sem remover o campo do validated_data
        Property.validate_rfid_tag(validated_data["rfid_tag"])
        return super().create(validated_data)


class ContractSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    property_name = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'id',
            'property',
            'supplier',
            'start_date',
            'end_date',
            'value',
            'supplier_name',
            'property_name'
        ]

    def get_supplier_name(self, obj):
        return obj.supplier.name

    def get_property_name(self, obj):
        return obj.property.name