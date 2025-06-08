from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_ride_view, name='book_ride'),
    path('detail/<int:ride_id>/', views.ride_detail_view, name='ride_detail'),
    path('history/', views.ride_history_view, name='ride_history'),
    path('cancel/<int:ride_id>/', views.cancel_ride_view, name='cancel_ride'),
    path('accept/<int:ride_id>/', views.accept_ride_view, name='accept_ride'),
    path('start/<int:ride_id>/', views.start_ride_view, name='start_ride'),
    path('complete/<int:ride_id>/', views.complete_ride_view, name='complete_ride'),
]
