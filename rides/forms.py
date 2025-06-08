from django import forms
from .models import Ride
from drivers.models import CabType

class RideBookingForm(forms.ModelForm):
    pickup_location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pickup Location',
        'id': 'pickup-location'
    }))
    drop_location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Drop Location',
        'id': 'drop-location'
    }))
    pickup_latitude = forms.DecimalField(widget=forms.HiddenInput(attrs={
        'id': 'pickup-latitude'
    }))
    pickup_longitude = forms.DecimalField(widget=forms.HiddenInput(attrs={
        'id': 'pickup-longitude'
    }))
    drop_latitude = forms.DecimalField(widget=forms.HiddenInput(attrs={
        'id': 'drop-latitude'
    }))
    drop_longitude = forms.DecimalField(widget=forms.HiddenInput(attrs={
        'id': 'drop-longitude'
    }))
    distance = forms.DecimalField(widget=forms.HiddenInput(attrs={
        'id': 'distance'
    }))
    cab_type = forms.ModelChoiceField(
        queryset=CabType.objects.all(),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = Ride
        fields = ['pickup_location', 'drop_location', 'pickup_latitude', 'pickup_longitude', 'drop_latitude', 'drop_longitude', 'distance', 'cab_type']

class RideCancellationForm(forms.Form):
    cancellation_reason = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Reason for cancellation',
        'rows': 3
    }))
