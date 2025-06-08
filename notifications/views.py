from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification
import json

@login_required
def notifications_view(request):
    # Get all notifications for the user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'notifications': notifications
    }
    
    return render(request, 'notifications/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id)
        
        # Check if the notification belongs to the user
        if notification.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        # Mark as read
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'status': 'success', 'message': 'Notification marked as read'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        # Update all unread notifications for the user
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        
        return JsonResponse({'status': 'success', 'message': 'All notifications marked as read'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def get_unread_notifications_count(request):
    # Count unread notifications
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({'count': count})
