from django import forms
from .models import DriverProfile, CabType

class DriverRegistrationForm(forms.ModelForm):
    cab_type = forms.ModelChoiceField(
        queryset=CabType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    license_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'License Number'
    }))
    vehicle_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Vehicle Number'
    }))
    vehicle_model = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Vehicle Model'
    }))
    vehicle_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Vehicle Year'
    }))
    vehicle_photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }), required=False)
    license_photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }), required=False)
    
    class Meta:
        model = DriverProfile
        fields = ['cab_type', 'license_number', 'vehicle_number', 'vehicle_model', 'vehicle_year', 'vehicle_photo', 'license_photo']

class DriverUpdateForm(forms.ModelForm):
    cab_type = forms.ModelChoiceField(
        queryset=CabType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    vehicle_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    vehicle_model = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    vehicle_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    vehicle_photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }), required=False)
    
    class Meta:
        model = DriverProfile
        fields = ['cab_type', 'vehicle_number', 'vehicle_model', 'vehicle_year', 'vehicle_photo']
