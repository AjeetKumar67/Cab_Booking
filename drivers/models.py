from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

class CabType(models.Model):
    name = models.CharField(max_length=50)
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2)
    base_fare = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='cab_types', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.price_per_km}/km"

class DriverProfile(models.Model):
    APPROVAL_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    AVAILABILITY_STATUS = (
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('on_trip', 'On Trip'),
    )
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='driver')
    cab_type = models.ForeignKey(CabType, on_delete=models.CASCADE, related_name='drivers')
    license_number = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.PositiveIntegerField()
    vehicle_photo = models.ImageField(upload_to='vehicle_pics', null=True, blank=True)
    license_photo = models.ImageField(upload_to='license_pics', null=True, blank=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='offline')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    total_rides = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.cab_type.name}"
