from django.contrib import admin
from .models import Ticket, HRRequest, Category  # <--- Ensure Category is here!

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'status', 'assigned_to', 'due_date')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('title', 'description')
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(HRRequest)
class HRRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'start_date', 'created_at')
    search_fields = ('full_name',)

# Add this section for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)