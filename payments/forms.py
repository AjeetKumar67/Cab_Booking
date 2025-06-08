from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    payment_mode = forms.ChoiceField(
        choices=Payment.PAYMENT_MODE,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = Payment
        fields = ['payment_mode']
