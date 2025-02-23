from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    """
    Formulário para o modelo Supplier.
    Permite a criação e edição de fornecedores com validações e estilizações personalizadas.
    """

    class Meta:
        model = Supplier
        fields = ['name', 'tax_id', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'placeholder': 'Digite 14 dígitos'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Digite 14 dígitos'}),
        }

    def clean_tax_id(self):
        """
        Valida o campo tax_id (CNPJ) para garantir que contenha exatamente 14 dígitos.
        Levanta ValidationError se o valor for inválido.
        """
        tax_id = self.cleaned_data.get('tax_id')
        if len(tax_id) != 14 or not tax_id.isdigit():
            raise forms.ValidationError("O CNPJ deve conter exatamente 14 dígitos numéricos.")
        return tax_id

    def clean_contact(self):
        """
        Valida o campo contact para garantir que contenha exatamente 14 dígitos.
        Levanta ValidationError se o valor for inválido.
        """
        contact = self.cleaned_data.get('contact')
        if len(contact) != 14 or not contact.isdigit():
            raise forms.ValidationError("O contato deve conter exatamente 14 dígitos numéricos.")
        return contact