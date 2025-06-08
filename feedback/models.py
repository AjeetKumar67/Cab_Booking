from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rides.models import Ride

class Feedback(models.Model):
    RATING_TYPE = (
        ('rider_to_driver', 'Rider to Driver'),
        ('driver_to_rider', 'Driver to Rider'),
    )
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    feedback_type = models.CharField(max_length=20, choices=RATING_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_feedback_type_display()} - Rating: {self.rating} (Ride {self.ride.id})"
    
    class Meta:
        unique_together = ('ride', 'feedback_type')
