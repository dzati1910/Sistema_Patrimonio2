from django import forms
from assets.models import Property, Category, Supplier, Department

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'category', 'supplier', 'department', 'rfid_tag']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'rfid_tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_rfid_tag(self):
        rfid_tag = self.cleaned_data.get('rfid_tag')
        # Verifica se já existe um objeto com o mesmo RFID
        if Property.objects.filter(rfid_tag=rfid_tag).exists():
            raise forms.ValidationError("Esse RFID já está sendo utilizado por outro bem.")
        return rfid_tag