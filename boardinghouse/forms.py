from django import forms

from boardinghouse.models import BoardingHouse, Room


class BoardingHouseForms(forms.ModelForm):
    class Meta:
        model = BoardingHouse
        fields = ('name', 'description', 'address', 'num_beds', 'num_baths', 'latitude', 'longitude', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'num_beds': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'num_baths': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('boardinghouse', 'name', 'price', 'num_bed', 'male_female','vacant', 'image')
        widgets = {
            'boardinghouse': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'num_bed': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'male_female': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'vacant': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
        }