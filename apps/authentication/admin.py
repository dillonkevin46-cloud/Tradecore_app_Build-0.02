from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'job_title')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__first_name')