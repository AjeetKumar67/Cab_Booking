from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.payment_history_view, name='payment_history'),
    path('invoice/<int:invoice_id>/', views.invoice_view, name='invoice'),
    path('update-payment-method/<int:payment_id>/', views.update_payment_method, name='update_payment_method'),
    path('download-invoice/<int:invoice_id>/', views.download_invoice, name='download_invoice'),
]
