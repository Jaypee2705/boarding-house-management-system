from django import forms

from homepage.models import Feedback


class FeedbackForms(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback',)
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control'})
        }
