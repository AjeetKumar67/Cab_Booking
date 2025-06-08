from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, UserProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.models import User
from drivers.forms import DriverRegistrationForm
from rides.models import Ride
from notifications.models import Notification

def home_view(request):
    from .forms import UserLoginForm, UserRegistrationForm
    login_form = UserLoginForm()
    register_form = UserRegistrationForm()
    return render(request, 'home.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect based on user role
                try:
                    if user.profile.role == 'admin':
                        return redirect('admin_dashboard')
                    elif user.profile.role == 'driver':
                        return redirect('driver_dashboard')
                    else:
                        return redirect('rider_dashboard')
                except UserProfile.DoesNotExist:
                    return redirect('rider_dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Create the user profile
            profile = UserProfile.objects.create(
                user=user,
                role=form.cleaned_data.get('role'),
                mobile=form.cleaned_data.get('mobile'),
                gender=form.cleaned_data.get('gender'),
                address=form.cleaned_data.get('address'),
                photo=request.FILES.get('photo')
            )
            
            # If registering as a driver, redirect to driver details
            if form.cleaned_data.get('role') == 'driver':
                login(request, user)
                messages.success(request, 'Your account has been created! Please complete your driver profile.')
                return redirect('driver_registration')
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created successfully.')
            return redirect('rider_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        messages.warning(request, 'Your user profile is incomplete. Please contact support.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update the User model
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            # Form will save the UserProfile
            profile = form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    
    return render(request, 'users/profile.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    
    try:
        profile = UserProfile.objects.get(user=user)
        if profile.role == 'admin':
            return redirect('admin_dashboard')
        elif profile.role == 'driver':
            return redirect('driver_dashboard')
        else:  # 'rider' or any other role
            return redirect('rider_dashboard')
    except UserProfile.DoesNotExist:
        # If no profile exists, show a message and render a basic dashboard
        messages.warning(request, 'Your user profile is incomplete. Please contact support.')
        return render(request, 'users/dashboard.html', {'incomplete_profile': True})

@login_required
def rider_dashboard_view(request):
    # Check if user has a profile
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'Your user profile is incomplete. Please contact support.')
        return render(request, 'users/dashboard.html', {'incomplete_profile': True})
    
    # If user is not a rider, but has a profile with another role, show a message but still render the dashboard
    if request.user.profile.role != 'rider':
        messages.info(request, f'Note: You are logged in as a {request.user.profile.get_role_display()}, not a Rider.')
    
    # Get recent rides
    recent_rides = Ride.objects.filter(rider=request.user.profile).order_by('-requested_at')[:5]
    
    # Get current ride (the most recent ride that is not completed or cancelled)
    current_ride = Ride.objects.filter(rider=request.user.profile, status__in=['requested', 'accepted', 'started']).order_by('-requested_at').first()
    
    # Check if the rider has already rated the driver for the current ride
    has_rated_driver = False
    if current_ride and current_ride.status == 'completed':
        has_rated_driver = current_ride.feedbacks.filter(feedback_type='rider_to_driver').exists()
    
    # Get unread notifications
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context = {
        'recent_rides': recent_rides,
        'current_ride': current_ride,
        'has_rated_driver': has_rated_driver,
        'notifications': notifications
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def admin_dashboard_view(request):
    # Check if user has a profile
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'Your user profile is incomplete. Please contact support.')
        return render(request, 'users/dashboard.html', {'incomplete_profile': True})
    
    # If user is not an admin, show a message but still render the dashboard with limited data
    if request.user.profile.role != 'admin':
        messages.info(request, f'Note: You are logged in as a {request.user.profile.get_role_display()}, not an Admin. Some admin features may be restricted.')
    
    # Get recent rides
    recent_rides = Ride.objects.all().order_by('-requested_at')[:10]
    
    # Get pending driver approvals
    from drivers.models import DriverProfile
    pending_drivers = DriverProfile.objects.filter(approval_status='pending').order_by('-created_at')
    
    context = {
        'recent_rides': recent_rides,
        'pending_drivers': pending_drivers,
    }
    
    return render(request, 'admin/dashboard.html', context)
