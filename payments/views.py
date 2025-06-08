from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Payment, Invoice
from rides.models import Ride
import json
from datetime import datetime
from decimal import Decimal

@login_required
def payment_history_view(request):
    # Check user role
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'User profile not found.')
        return redirect('dashboard')
    
    if request.user.profile.role == 'rider':
        # Get all rides for the rider
        rides = Ride.objects.filter(rider=request.user.profile, status='completed')
        payments = Payment.objects.filter(ride__in=rides).order_by('-created_at')
    
    elif request.user.profile.role == 'driver':
        try:
            driver = request.user.profile.driver
            # Get all rides for the driver
            rides = Ride.objects.filter(driver=driver, status='completed')
            payments = Payment.objects.filter(ride__in=rides).order_by('-created_at')
        except:
            messages.warning(request, 'Driver profile not found.')
            return redirect('dashboard')
    
    elif request.user.profile.role == 'admin':
        # Get all payments
        payments = Payment.objects.all().order_by('-created_at')
    
    else:
        payments = []
    
    context = {
        'payments': payments
    }
    
    return render(request, 'payments/payment_history.html', context)

@login_required
def invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check if user is authorized to view this invoice
    if request.user.profile.role == 'rider':
        if invoice.payment.ride.rider != request.user.profile:
            messages.warning(request, 'You are not authorized to view this invoice.')
            return redirect('dashboard')
    
    elif request.user.profile.role == 'driver':
        try:
            driver = request.user.profile.driver
            if invoice.payment.ride.driver != driver:
                messages.warning(request, 'You are not authorized to view this invoice.')
                return redirect('dashboard')
        except:
            messages.warning(request, 'Driver profile not found.')
            return redirect('dashboard')
    
    elif request.user.profile.role != 'admin':
        messages.warning(request, 'You are not authorized to view this invoice.')
        return redirect('dashboard')
    
    context = {
        'invoice': invoice
    }
    
    return render(request, 'payments/invoice.html', context)

@login_required
def update_payment_method(request, payment_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method = data.get('payment_method')
            
            if payment_method not in ['cash', 'card', 'upi']:
                return JsonResponse({'status': 'error', 'message': 'Invalid payment method'}, status=400)
            
            payment = get_object_or_404(Payment, id=payment_id)
            
            # Check if user is authorized to update this payment
            if request.user.profile.role == 'rider':
                if payment.ride.rider != request.user.profile:
                    return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
            elif request.user.profile.role == 'driver':
                try:
                    driver = request.user.profile.driver
                    if payment.ride.driver != driver:
                        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
                except:
                    return JsonResponse({'status': 'error', 'message': 'Driver profile not found'}, status=404)
            
            elif request.user.profile.role != 'admin':
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
            payment.payment_method = payment_method
            payment.save()
            
            return JsonResponse({'status': 'success', 'message': 'Payment method updated successfully'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check if user is authorized to download this invoice
    if request.user.profile.role == 'rider':
        if invoice.payment.ride.rider != request.user.profile:
            messages.warning(request, 'You are not authorized to download this invoice.')
            return redirect('dashboard')
    
    elif request.user.profile.role == 'driver':
        try:
            driver = request.user.profile.driver
            if invoice.payment.ride.driver != driver:
                messages.warning(request, 'You are not authorized to download this invoice.')
                return redirect('dashboard')
        except:
            messages.warning(request, 'Driver profile not found.')
            return redirect('dashboard')
    
    elif request.user.profile.role != 'admin':
        messages.warning(request, 'You are not authorized to download this invoice.')
        return redirect('dashboard')
    
    # In a real application, we would generate a PDF and return it
    # For this demo, we'll just render the invoice page
    context = {
        'invoice': invoice,
        'is_download': True
    }
    
    return render(request, 'payments/invoice.html', context)
