from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'make', 'model', 'serial_number', 'site', 'ip_address', 'is_monitored')
    list_filter = ('site', 'is_monitored', 'make')
    search_fields = ('device_name', 'serial_number', 'ip_address')