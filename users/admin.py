from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'mobile', 'gender', 'is_verified', 'created_at')
    list_filter = ('role', 'gender', 'is_verified')
    search_fields = ('user__username', 'user__email', 'mobile')
    readonly_fields = ('created_at', 'updated_at')
