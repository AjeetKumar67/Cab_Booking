from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DriverRegistrationForm, DriverUpdateForm
from .models import DriverProfile, CabType
from users.models import UserProfile
from rides.models import Ride
from notifications.models import Notification
from django.http import JsonResponse, HttpResponse
import json
from decimal import Decimal

def driver_registration_form(request):
    """
    Return the driver registration form as HTML for AJAX requests
    """
    form = DriverRegistrationForm()
    return render(request, 'drivers/partials/driver_form.html', {'form': form})

@login_required
def driver_registration_view(request):
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        messages.warning(request, 'You are not authorized to register as a driver.')
        return redirect('dashboard')
    
    # Check if driver profile already exists
    try:
        driver = request.user.profile.driver
        messages.info(request, 'You have already registered as a driver.')
        return redirect('driver_dashboard')
    except DriverProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            driver_profile = form.save(commit=False)
            driver_profile.user_profile = request.user.profile
            driver_profile.save()
            
            messages.success(request, 'Your driver profile has been created successfully. Please wait for admin approval.')
            return redirect('driver_dashboard')
    else:
        form = DriverRegistrationForm()
    
    return render(request, 'drivers/registration.html', {'form': form})

@login_required
def driver_dashboard_view(request):
    # Check if user has a profile
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'Your user profile is incomplete. Please contact support.')
        return render(request, 'users/dashboard.html', {'incomplete_profile': True})
    
    # If user is not a driver, show a message
    if request.user.profile.role != 'driver':
        messages.info(request, f'Note: You are logged in as a {request.user.profile.get_role_display()}, not a Driver. Some driver features may be restricted.')
    
    # Check if driver profile exists
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        # If the user is a driver but doesn't have a driver profile, redirect to registration
        if request.user.profile.role == 'driver':
            messages.info(request, 'Please complete your driver profile to access the driver dashboard.')
            return redirect('driver_registration')
        else:
            # For non-drivers, just show an informational message
            driver = None
            messages.info(request, 'You do not have a driver profile.')
    
    # Get recent trips if driver profile exists
    if driver:
        recent_trips = Ride.objects.filter(driver=driver).order_by('-requested_at')[:5]
        current_trip = Ride.objects.filter(driver=driver, status__in=['accepted', 'started']).first()
    else:
        recent_trips = []
        current_trip = None
    
    # Get unread notifications
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context = {
        'driver': driver,
        'recent_trips': recent_trips,
        'current_trip': current_trip,
        'notifications': notifications
    }
    
    return render(request, 'drivers/dashboard.html', context)

@login_required
def update_driver_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = Decimal(data.get('latitude'))
            longitude = Decimal(data.get('longitude'))
            
            # Get driver profile
            driver = request.user.profile.driver
            
            # Update location
            driver.current_latitude = latitude
            driver.current_longitude = longitude
            driver.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def toggle_driver_status(request):
    if request.method == 'POST':
        try:
            # Get driver profile
            driver = request.user.profile.driver
            
            # Toggle availability
            if driver.availability_status == 'offline':
                driver.availability_status = 'online'
                message = 'You are now online and available for rides.'
            else:
                driver.availability_status = 'offline'
                message = 'You are now offline and unavailable for rides.'
            
            driver.save()
            
            messages.success(request, message)
            return redirect('driver_dashboard')
        except Exception as e:
            messages.error(request, str(e))
    
    return redirect('driver_dashboard')

@login_required
def update_driver_profile(request):
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        messages.warning(request, 'You are not authorized to update driver profile.')
        return redirect('dashboard')
    
    # Check if driver profile exists
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        return redirect('driver_registration')
    
    if request.method == 'POST':
        form = DriverUpdateForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your driver profile has been updated successfully.')
            return redirect('driver_dashboard')
    else:
        form = DriverUpdateForm(instance=driver)
    
    return render(request, 'drivers/update_profile.html', {'form': form})
