from django import forms
from .models import NetworkTarget, MonitorCategory, SystemSetting, DailyChecklist

class MonitorCategoryForm(forms.ModelForm):
    class Meta:
        model = MonitorCategory
        fields = ['name', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Servers'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-server'}),
        }

class NetworkTargetForm(forms.ModelForm):
    class Meta:
        model = NetworkTarget
        fields = ['name', 'host', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device Name'}),
            'host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.1 or hostname'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

# --- NEW FORMS (Settings & Checklist) ---

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['report_email']
        widgets = {
            'report_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'manager@company.com'})
        }

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = DailyChecklist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Task Name...'})
        }