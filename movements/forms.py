# movements/forms.py
from django import forms
from .models import Movement
from django.core.exceptions import ValidationError


class MovementForm(forms.ModelForm):
    """
    Formulário para o modelo Movement.
    Permite a criação e edição de movimentações de bens entre departamentos.
    Inclui validações personalizadas para garantir a consistência dos dados.
    """

    class Meta:
        model = Movement
        fields = ['property', 'origin_department', 'destination_department']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-select'}),
            'origin_department': forms.Select(attrs={'class': 'form-select'}),
            'destination_department': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        """
        Validações personalizadas para o formulário:
        1. Departamentos de origem e destino devem ser diferentes.
        2. O bem deve estar localizado no departamento de origem especificado.
        """
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin_department')
        destination = cleaned_data.get('destination_department')
        property_obj = cleaned_data.get('property')

        # Retorna os dados se algum campo estiver faltando
        if not all([origin, destination, property_obj]):
            return cleaned_data

        # Validação 1: Departamentos diferentes
        if origin == destination:
            self.add_error(
                'destination_department',  # Campo específico
                "Departamentos de origem e destino devem ser diferentes"
            )

        # Validação 2: Bem está no departamento de origem
        if property_obj.department != origin:
            self.add_error(
                'origin_department',  # Campo específico
                "O bem não está localizado no departamento de origem especificado"
            )

        return cleaned_data