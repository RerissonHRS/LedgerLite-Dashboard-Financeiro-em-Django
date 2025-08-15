from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'product', 'category', 'unit_price', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'step':'0.01','class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
