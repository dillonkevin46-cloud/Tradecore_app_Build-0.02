from django import forms
from .models import ChecklistItem, ReportRecipient  # <--- Crucial: Add ReportRecipient here

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Check Server Room Temperature'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        help_texts = {
            'is_active': 'Uncheck this to hide the item without deleting it.'
        }

class RecipientForm(forms.ModelForm):
    class Meta:
        model = ReportRecipient
        fields = ['name', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IT Manager'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'manager@tradecore.co.za'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }