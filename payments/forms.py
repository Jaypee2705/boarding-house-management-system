from django import forms

from payments.models import Bills


class BillsForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ['room', 'bills', 'rate']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'bills': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.TextInput(attrs={'class': 'form-control'}),
        }