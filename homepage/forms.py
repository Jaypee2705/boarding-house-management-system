from django import forms
from django.contrib.auth.models import User

from homepage.models import Feedback, Notice


class FeedbackForms(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback',)
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control'})
        }

class NoticeForms(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'notice')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'notice': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),

        }