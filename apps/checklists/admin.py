from django.contrib import admin
from .models import ChecklistItem, DailyReport, ReportEntry, ReportRecipient

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    # Fixed: Removed 'email_sent' which caused the error
    list_display = ('technician', 'date', 'created_at')
    list_filter = ('date', 'technician')
    search_fields = ('technician__username', 'notes')

@admin.register(ReportEntry)
class ReportEntryAdmin(admin.ModelAdmin):
    list_display = ('report', 'item', 'status')
    list_filter = ('status', 'item')

@admin.register(ReportRecipient)
class ReportRecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')
    list_filter = ('is_active',)