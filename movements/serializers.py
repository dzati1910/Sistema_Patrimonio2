from rest_framework import serializers
from .models import Movement

class MovementSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name', read_only=True)
    origin_department_name = serializers.CharField(source='origin_department.name', read_only=True)
    destination_department_name = serializers.CharField(source='destination_department.name', read_only=True)

    class Meta:
        model = Movement
        fields = [
            'id',
            'property',
            'property_name',
            'origin_department',
            'origin_department_name',
            'destination_department',
            'destination_department_name',
            'timestamp',
        ]
        read_only_fields = [
            'id',
            'timestamp',
            'property_name',
            'origin_department_name',
            'destination_department_name'
        ]

    def validate(self, data):
        origin = data.get('origin_department')
        destination = data.get('destination_department')
        if origin == destination:
            raise serializers.ValidationError(
                "Origin and destination departments cannot be the same."
            )
        return data