from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Campo não retornado na resposta
    is_department_responsible = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'tax_id', 'is_department_responsible']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            tax_id=validated_data.get('tax_id')
        )
        return user

    def get_is_department_responsible(self, obj):
        return obj.is_department_responsible()