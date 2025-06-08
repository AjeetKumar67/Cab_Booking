from django.contrib import admin
from .models import Payment, Invoice

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ride', 'amount', 'payment_mode', 'status', 'paid_at', 'created_at')
    list_filter = ('payment_mode', 'status')
    search_fields = ('ride__id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'payment', 'base_fare', 'distance_fare', 'waiting_charges', 'taxes', 'total_amount', 'created_at')
    search_fields = ('invoice_number', 'payment__ride__id')
    readonly_fields = ('created_at',)
