from django import forms

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
        fields = ('title', 'notice', 'boardinghouse')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'notice': forms.Textarea(attrs={'class': 'form-control'}),
            'boardinghouse': forms.Select(attrs={'class': 'form-control'}),
        }