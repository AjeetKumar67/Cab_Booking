from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5
        })
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your feedback about the ride',
            'rows': 3
        }),
        required=False
    )
    
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
