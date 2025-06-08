from django.contrib import admin
from .models import DriverProfile, CabType

@admin.register(CabType)
class CabTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_km', 'base_fare', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'cab_type', 'approval_status', 'availability_status', 'total_rides', 'average_rating')
    list_filter = ('approval_status', 'availability_status', 'cab_type')
    search_fields = ('user_profile__user__username', 'user_profile__user__email', 'license_number', 'vehicle_number')
    readonly_fields = ('created_at', 'updated_at', 'total_rides', 'average_rating')
