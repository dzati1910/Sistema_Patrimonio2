from django import forms
from .models import Maintenance


class AdminMaintenanceForm(forms.ModelForm):
    """
    Formulário administrativo para o modelo Maintenance.
    Permite a criação e edição de manutenções com todos os campos disponíveis.
    Inclui validações personalizadas para datas e status.
    """

    class Meta:
        model = Maintenance
        fields = ['property', 'scheduled_date', 'completion_date', 'cost', 'description', 'status']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={
                'type': 'date',  # Adiciona explicitamente o type='date'
                'class': 'form-control'
            }),
            'completion_date': forms.DateInput(attrs={
                'type': 'date',  # Adiciona explicitamente o type='date'
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário e adiciona a classe 'form-control' a todos os campos.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        """
        Validações personalizadas para o formulário:
        - Data de conclusão é obrigatória para manutenções com status "Completado".
        - A data de conclusão não pode ser anterior à data agendada.
        """
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completion_date = cleaned_data.get('completion_date')
        scheduled_date = cleaned_data.get('scheduled_date')

        # Validação para status "Completado"
        if status == 'Completado' and not completion_date:
            self.add_error('completion_date', 'Data de conclusão é obrigatória para manutenções completadas')

        # Validação de datas
        if scheduled_date and completion_date:
            if completion_date < scheduled_date:
                self.add_error('completion_date', 'A data de conclusão não pode ser anterior à data agendada')

        return cleaned_data


class MaintenanceForm(forms.ModelForm):
    """
    Formulário simplificado para o modelo Maintenance.
    Permite a edição de campos específicos, como data de conclusão, custo, descrição e status.
    Inclui validações personalizadas para datas e status.
    """

    class Meta:
        model = Maintenance
        fields = ['completion_date', 'cost', 'description', 'status']
        widgets = {
            'completion_date': forms.DateInput(attrs={
                'type': 'date',  # Adiciona explicitamente o type='date'
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário e adiciona a classe 'form-control' a todos os campos.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        """
        Validações personalizadas para o formulário:
        - Data de conclusão é obrigatória para manutenções com status "Completado".
        - A data de conclusão não pode ser anterior à data agendada.
        """
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completion_date = cleaned_data.get('completion_date')

        # Obter dados da instância existente
        scheduled_date = self.instance.scheduled_date if self.instance else None

        # Validação de conclusão obrigatória
        if status == 'Completado' and not completion_date:
            self.add_error('completion_date', 'Data de conclusão é obrigatória para manutenções completadas')

        # Validação de datas
        if scheduled_date and completion_date:
            if completion_date < scheduled_date:
                self.add_error('completion_date', 'A data de conclusão não pode ser anterior à data agendada')

        return cleaned_data