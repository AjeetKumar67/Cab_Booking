from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.driver_registration_view, name='driver_registration'),
    path('registration-form/', views.driver_registration_form, name='driver_registration_form'),
    path('dashboard/', views.driver_dashboard_view, name='driver_dashboard'),
    path('update-location/', views.update_driver_location, name='update_driver_location'),
    path('toggle-status/', views.toggle_driver_status, name='toggle_driver_status'),
    path('update-profile/', views.update_driver_profile, name='update_driver_profile'),
]
