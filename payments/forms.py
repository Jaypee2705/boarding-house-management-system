from django import forms

from payments.models import Bills, Payments

BILL_CHOICES =(
        ('Electricity', 'Electricity'),
        ('Water', 'Water'),
        ('Internet', 'Internet'),
        ('Cable', 'Cables'),
        ('Others', 'Others')
    )
class BillsForm(forms.ModelForm):


    class Meta:
        model = Bills
        fields = [ 'bills', 'rate']
        widgets = {

            'bills': forms.Select(choices=BILL_CHOICES , attrs={'class': 'form-control'}),
            'rate': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ['amount', 'note', 'mode']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'mode': forms.TextInput(attrs={'class': 'form-control'}),
        }
