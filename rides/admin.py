from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'pickup_location', 'drop_location', 'status', 'distance', 'estimated_fare', 'final_fare', 'requested_at')
    list_filter = ('status', 'cab_type')
    search_fields = ('rider__user__username', 'driver__user_profile__user__username', 'pickup_location', 'drop_location')
    readonly_fields = ('requested_at', 'accepted_at', 'started_at', 'completed_at', 'cancelled_at')
