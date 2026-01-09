from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet

class PasswordEntry(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Office 365 Admin")
    username = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=500) # Stores the gibberish
    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Encrypts the password before saving"""
        f = Fernet(settings.ENCRYPTION_KEY)
        self.encrypted_password = f.encrypt(raw_password.encode()).decode()

    def get_password(self):
        """Decrypts the password for viewing"""
        try:
            f = Fernet(settings.ENCRYPTION_KEY)
            return f.decrypt(self.encrypted_password.encode()).decode()
        except:
            return "ERROR: Could not decrypt"

    def __str__(self):
        return f"{self.title} ({self.username})"