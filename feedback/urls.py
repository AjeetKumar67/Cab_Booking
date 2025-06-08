from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:ride_id>/', views.submit_feedback_view, name='submit_feedback'),
    path('driver/', views.driver_feedback_view, name='driver_feedback'),
]
