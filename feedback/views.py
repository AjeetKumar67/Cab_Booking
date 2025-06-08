from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Feedback
from .forms import FeedbackForm
from rides.models import Ride
from drivers.models import DriverProfile
from notifications.models import Notification
from decimal import Decimal

@login_required
def submit_feedback_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if user is the rider
    if not hasattr(request.user, 'profile') or ride.rider != request.user.profile:
        messages.warning(request, 'You are not authorized to submit feedback for this ride.')
        return redirect('dashboard')
    
    # Check if ride is completed
    if ride.status != 'completed':
        messages.warning(request, 'You can only submit feedback for completed rides.')
        return redirect('ride_detail', ride_id=ride.id)
    
    # Check if feedback already exists
    existing_feedback = Feedback.objects.filter(ride=ride, user=request.user).first()
    if existing_feedback:
        messages.info(request, 'You have already submitted feedback for this ride.')
        return redirect('ride_detail', ride_id=ride.id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ride = ride
            feedback.user = request.user
            feedback.driver = ride.driver
            feedback.save()
            
            # Update driver average rating
            update_driver_rating(ride.driver)
            
            # Notify driver
            create_notification(
                user=ride.driver.user_profile.user,
                title='New Feedback',
                message=f'You received a {feedback.rating}-star rating for ride #{ride.id}'
            )
            
            messages.success(request, 'Your feedback has been submitted successfully.')
            return redirect('ride_detail', ride_id=ride.id)
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'ride': ride
    }
    
    return render(request, 'feedback/submit_feedback.html', context)

@login_required
def driver_feedback_view(request):
    # Check if user is a driver
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        messages.warning(request, 'Only drivers can view their feedback.')
        return redirect('dashboard')
    
    try:
        driver = request.user.profile.driver
    except DriverProfile.DoesNotExist:
        messages.warning(request, 'Driver profile not found.')
        return redirect('dashboard')
    
    # Get all feedback for the driver
    feedback = Feedback.objects.filter(driver=driver).order_by('-created_at')
    
    context = {
        'feedback': feedback,
        'driver': driver
    }
    
    return render(request, 'feedback/driver_feedback.html', context)

def update_driver_rating(driver):
    """Update the driver's average rating"""
    feedback_list = Feedback.objects.filter(driver=driver)
    
    if feedback_list:
        total_rating = sum(feedback.rating for feedback in feedback_list)
        average_rating = Decimal(total_rating) / Decimal(feedback_list.count())
        
        # Update driver's average rating
        driver.average_rating = average_rating.quantize(Decimal('0.01'))  # Round to 2 decimal places
        driver.save()

def create_notification(user, title, message):
    """Create a notification for a user"""
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
