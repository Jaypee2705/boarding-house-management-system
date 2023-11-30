from django import forms

from payments.models import Bills, Payments


class BillsForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ['room', 'bills', 'rate']
        widgets = {

            'room': forms.Select(attrs={'class': 'form-control'}),
            'bills': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ['room', 'tenant', 'amount', 'note', 'mode']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'mode': forms.TextInput(attrs={'class': 'form-control'}),
        }