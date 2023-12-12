from django import forms

from payments.models import Bills, Payments, TransientPayment

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

class TransientPaymentForm(forms.ModelForm):
    class Meta:
        model = TransientPayment
        fields = ['room', 'transient', 'address', 'contact', 'days', 'amount', 'note', 'mode']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'transient': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'pattern': "(^\+639\d{9}$)|(^\d{11}$)" , 'title': "Please enter a valid Philippine contact number in the format: +639123456789 or 09123456789"}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'mode': forms.TextInput(attrs={'class': 'form-control'}),
        }
