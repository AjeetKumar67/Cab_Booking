from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('ride', 'rating', 'feedback_type', 'created_at')
    list_filter = ('rating', 'feedback_type')
    search_fields = ('ride__id', 'comment')
    readonly_fields = ('created_at',)
