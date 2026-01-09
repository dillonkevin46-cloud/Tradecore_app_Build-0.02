from django import forms
from .models import PasswordEntry

class PasswordEntryForm(forms.ModelForm):
    # We add a fake field for the password input so we can handle encryption manually
    password_input = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password",
        required=False # False so we can leave it empty on 'Edit' if not changing
    )

    class Meta:
        model = PasswordEntry
        fields = ['title', 'username', 'website', 'notes'] # Exclude encrypted_password
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Router Login'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'admin'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }