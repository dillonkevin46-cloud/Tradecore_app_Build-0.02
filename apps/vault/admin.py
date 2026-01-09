from django.contrib import admin
from .models import PasswordEntry

@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'website', 'created_at')
    search_fields = ('title', 'username')
    exclude = ('encrypted_password',)