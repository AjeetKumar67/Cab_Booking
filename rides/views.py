from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Ride
from .forms import RideBookingForm, RideCancellationForm
from drivers.models import DriverProfile, CabType
from notifications.models import Notification
from payments.models import Payment, Invoice
import json
from decimal import Decimal
from datetime import datetime
import random

@login_required
def book_ride_view(request):
    # Check if user is a rider
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'rider':
        messages.warning(request, 'Only riders can book rides.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RideBookingForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.rider = request.user.profile
            
            # Calculate the estimated fare
            ride.estimated_fare = ride.calculate_fare()
            ride.save()
            
            # Find nearby drivers
            find_and_notify_drivers(ride)
            
            messages.success(request, 'Your ride request has been submitted. Looking for drivers...')
            return redirect('ride_detail', ride_id=ride.id)
    else:
        form = RideBookingForm()
    
    context = {
        'form': form,
        'cab_types': CabType.objects.all()
    }
    
    return render(request, 'rides/book_ride.html', context)

@login_required
def ride_detail_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if user is the rider, driver, or admin
    is_rider = hasattr(request.user, 'profile') and ride.rider == request.user.profile
    is_driver = hasattr(request.user, 'profile') and hasattr(request.user.profile, 'driver') and ride.driver == request.user.profile.driver
    is_admin = hasattr(request.user, 'profile') and request.user.profile.role == 'admin'
    
    if not (is_rider or is_driver or is_admin):
        messages.warning(request, 'You are not authorized to view this ride.')
        return redirect('dashboard')
    
    context = {
        'ride': ride,
        'is_rider': is_rider,
        'is_driver': is_driver,
        'is_admin': is_admin
    }
    
    return render(request, 'rides/ride_detail.html', context)

@login_required
def ride_history_view(request):
    # Check user role
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'User profile not found.')
        return redirect('dashboard')
    
    if request.user.profile.role == 'rider':
        rides = Ride.objects.filter(rider=request.user.profile).order_by('-requested_at')
    elif request.user.profile.role == 'driver':
        try:
            driver = request.user.profile.driver
            rides = Ride.objects.filter(driver=driver).order_by('-requested_at')
        except DriverProfile.DoesNotExist:
            messages.warning(request, 'Driver profile not found.')
            return redirect('dashboard')
    elif request.user.profile.role == 'admin':
        rides = Ride.objects.all().order_by('-requested_at')
    else:
        rides = []
    
    context = {
        'rides': rides
    }
    
    return render(request, 'rides/ride_history.html', context)

@login_required
def cancel_ride_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if user is the rider or driver
    is_rider = hasattr(request.user, 'profile') and ride.rider == request.user.profile
    is_driver = hasattr(request.user, 'profile') and hasattr(request.user.profile, 'driver') and ride.driver == request.user.profile.driver
    
    if not (is_rider or is_driver):
        messages.warning(request, 'You are not authorized to cancel this ride.')
        return redirect('dashboard')
    
    # Check if ride can be cancelled
    if ride.status not in ['requested', 'accepted']:
        messages.warning(request, 'This ride cannot be cancelled at this stage.')
        return redirect('ride_detail', ride_id=ride.id)
    
    if request.method == 'POST':
        form = RideCancellationForm(request.POST)
        if form.is_valid():
            ride.status = 'cancelled'
            ride.cancelled_at = datetime.now()
            ride.cancelled_by = request.user
            ride.cancellation_reason = form.cleaned_data.get('cancellation_reason')
            ride.save()
            
            # Notify the other party
            if is_rider and ride.driver:
                create_notification(
                    user=ride.driver.user_profile.user,
                    title='Ride Cancelled',
                    message=f'Ride #{ride.id} has been cancelled by the rider.'
                )
            elif is_driver and ride.rider:
                create_notification(
                    user=ride.rider.user,
                    title='Ride Cancelled',
                    message=f'Ride #{ride.id} has been cancelled by the driver.'
                )
            
            messages.success(request, 'The ride has been cancelled successfully.')
            return redirect('dashboard')
    else:
        form = RideCancellationForm()
    
    context = {
        'ride': ride,
        'form': form
    }
    
    return render(request, 'rides/cancel_ride.html', context)

@login_required
def accept_ride_view(request, ride_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'status': 'error', 'message': 'Only drivers can accept rides'}, status=403)
    
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Driver profile not found'}, status=404)
    
    # Check if driver is available
    if driver.availability_status != 'online':
        return JsonResponse({'status': 'error', 'message': 'You must be online to accept rides'}, status=403)
    
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if ride can be accepted
    if ride.status != 'requested':
        return JsonResponse({'status': 'error', 'message': 'This ride cannot be accepted'}, status=400)
    
    # Accept the ride
    ride.driver = driver
    ride.status = 'accepted'
    ride.accepted_at = datetime.now()
    ride.save()
    
    # Update driver status
    driver.availability_status = 'on_trip'
    driver.save()
    
    # Notify rider
    create_notification(
        user=ride.rider.user,
        title='Ride Accepted',
        message=f'Your ride #{ride.id} has been accepted by {driver.user_profile.user.get_full_name()}.'
    )
    
    return JsonResponse({'status': 'success', 'message': 'Ride accepted successfully'})

@login_required
def start_ride_view(request, ride_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'status': 'error', 'message': 'Only drivers can start rides'}, status=403)
    
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Driver profile not found'}, status=404)
    
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if ride belongs to the driver
    if ride.driver != driver:
        return JsonResponse({'status': 'error', 'message': 'This ride does not belong to you'}, status=403)
    
    # Check if ride can be started
    if ride.status != 'accepted':
        return JsonResponse({'status': 'error', 'message': 'This ride cannot be started'}, status=400)
    
    # Start the ride
    ride.status = 'started'
    ride.started_at = datetime.now()
    ride.save()
    
    # Notify rider
    create_notification(
        user=ride.rider.user,
        title='Ride Started',
        message=f'Your ride #{ride.id} has been started.'
    )
    
    return JsonResponse({'status': 'success', 'message': 'Ride started successfully'})

@login_required
def complete_ride_view(request, ride_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'status': 'error', 'message': 'Only drivers can complete rides'}, status=403)
    
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Driver profile not found'}, status=404)
    
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if ride belongs to the driver
    if ride.driver != driver:
        return JsonResponse({'status': 'error', 'message': 'This ride does not belong to you'}, status=403)
    
    # Check if ride can be completed
    if ride.status != 'started':
        return JsonResponse({'status': 'error', 'message': 'This ride cannot be completed'}, status=400)
    
    # Complete the ride
    ride.status = 'completed'
    ride.completed_at = datetime.now()
    
    # Calculate final fare (with slight randomness to simulate real-world scenarios)
    variation = random.uniform(-0.05, 0.1)  # -5% to +10%
    ride.final_fare = ride.estimated_fare * (1 + Decimal(variation))
    ride.final_fare = ride.final_fare.quantize(Decimal('0.01'))  # Round to 2 decimal places
    
    ride.save()
    
    # Create payment
    create_payment(ride)
    
    # Update driver status and statistics
    driver.availability_status = 'online'
    driver.total_rides += 1
    driver.save()
    
    # Notify rider
    create_notification(
        user=ride.rider.user,
        title='Ride Completed',
        message=f'Your ride #{ride.id} has been completed. Total fare: ₹{ride.final_fare}'
    )
    
    return JsonResponse({'status': 'success', 'message': 'Ride completed successfully', 'final_fare': str(ride.final_fare)})

def find_and_notify_drivers(ride):
    """Find nearby drivers and notify them about the ride request"""
    # In a real application, this would involve geospatial queries
    # For this demo, we'll simply notify all online drivers of the same cab type
    available_drivers = DriverProfile.objects.filter(
        cab_type=ride.cab_type,
        availability_status='online',
        approval_status='approved'
    )
    
    for driver in available_drivers:
        create_notification(
            user=driver.user_profile.user,
            title='New Ride Request',
            message=f'New ride request from {ride.pickup_location} to {ride.drop_location}. Distance: {ride.distance} km'
        )

def create_notification(user, title, message):
    """Create a notification for a user"""
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )

def create_payment(ride):
    """Create a payment record and invoice for a completed ride"""
    # Create payment
    payment = Payment.objects.create(
        ride=ride,
        amount=ride.final_fare,
        payment_method='cash',  # Default to cash
        status='completed'
    )
    
    # Create invoice
    Invoice.objects.create(
        payment=payment,
        invoice_number=f'INV-{ride.id}-{payment.id}',
        amount=ride.final_fare,
        rider_name=ride.rider.user.get_full_name(),
        driver_name=ride.driver.user_profile.user.get_full_name() if ride.driver else 'N/A',
        pickup_location=ride.pickup_location,
        drop_location=ride.drop_location,
        distance=ride.distance,
        ride_date=ride.completed_at
    )
