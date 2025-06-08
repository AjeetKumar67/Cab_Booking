from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
from drivers.models import DriverProfile, CabType

class Ride(models.Model):
    RIDE_STATUS = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    rider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='trips', null=True, blank=True)
    cab_type = models.ForeignKey(CabType, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    drop_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    drop_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    distance = models.DecimalField(max_digits=8, decimal_places=2)  # in kilometers
    duration = models.PositiveIntegerField(null=True, blank=True)  # in minutes
    estimated_fare = models.DecimalField(max_digits=8, decimal_places=2)
    final_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=RIDE_STATUS, default='requested')
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_rides')
    cancellation_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Ride {self.id} - {self.pickup_location} to {self.drop_location} ({self.status})"
    
    def calculate_fare(self):
        """Calculate the fare based on cab type, distance and base fare"""
        return self.cab_type.base_fare + (self.distance * self.cab_type.price_per_km)
