from django.contrib import admin
from .models import MonitorCategory, NetworkTarget, DailyChecklist, SystemSetting

@admin.register(MonitorCategory)
class MonitorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(NetworkTarget)
class NetworkTargetAdmin(admin.ModelAdmin):
    # Fixed: Changed 'last_check' to 'last_checked' to match the model
    list_display = ('name', 'host', 'category', 'is_active', 'is_online', 'response_time', 'last_checked')
    list_filter = ('category', 'is_online', 'is_active')
    search_fields = ('name', 'host')

@admin.register(DailyChecklist)
class DailyChecklistAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_checked', 'last_checked')
    list_editable = ('is_checked',)

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'report_email')