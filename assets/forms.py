from django import forms
from .models import *

class ContractForm(forms.ModelForm):
    """
    Formulário para o modelo Contract.
    Permite a criação e edição de contratos associados a propriedades e fornecedores.
    """

    class Meta:
        model = Contract
        fields = ['property', 'supplier', 'start_date', 'end_date', 'value']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Usa input do tipo 'date' para datas
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CategoryForm(forms.ModelForm):
    """
    Formulário para o modelo Category.
    Permite a criação e edição de categorias de propriedades.
    """

    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Adiciona classe CSS para estilização
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário, chamando o método da classe pai."""
        super().__init__(*args, **kwargs)


class DepartmentForm(forms.ModelForm):
    """
    Formulário para o modelo Department.
    Permite a criação e edição de departamentos, incluindo nome, localização e responsável.
    """

    class Meta:
        model = Department
        fields = ['name', 'location', 'responsible_person']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_person': forms.Select(attrs={'class': 'form-select'}),  # Usa um dropdown estilizado
        }


class AdminPropertyForm(forms.ModelForm):
    """
    Formulário para o modelo Property, destinado ao uso administrativo.
    Permite a criação e edição de propriedades com todos os campos relevantes.
    """

    class Meta:
        model = Property
        fields = ['name', 'category', 'supplier', 'department', 'rfid_tag', 'quantity', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'rfid_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_rfid_tag(self):
        """
        Valida a tag RFID para garantir que não está sendo usada por outra propriedade.
        Levanta ValidationError se a tag já estiver em uso.
        """
        rfid_tag = self.cleaned_data.get('rfid_tag')

        # Exclui a instância atual durante a validação (cenário de atualização)
        if self.instance.pk:
            property_exists = Property.objects.filter(
                rfid_tag=rfid_tag
            ).exclude(
                pk=self.instance.pk
            ).exists()
        else:
            property_exists = Property.objects.filter(rfid_tag=rfid_tag).exists()

        if property_exists:
            raise forms.ValidationError("Esse RFID já está sendo utilizado por outro bem.")
        return rfid_tag


class PropertyForm(forms.ModelForm):
    """
    Formulário simplificado para o modelo Property.
    Permite a edição de quantidade e valor da propriedade.
    """

    class Meta:
        model = Property
        fields = ['quantity', 'value']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_rfid_tag(self):
        """
        Valida a tag RFID para garantir que não está sendo usada por outra propriedade.
        Levanta ValidationError se a tag já estiver em uso.
        """
        rfid_tag = self.cleaned_data.get('rfid_tag')

        # Exclui a instância atual durante a validação (cenário de atualização)
        if self.instance.pk:
            property_exists = Property.objects.filter(
                rfid_tag=rfid_tag
            ).exclude(
                pk=self.instance.pk
            ).exists()
        else:
            property_exists = Property.objects.filter(rfid_tag=rfid_tag).exists()

        if property_exists:
            raise forms.ValidationError("Esse RFID já está sendo utilizado por outro bem.")
        return rfid_tag