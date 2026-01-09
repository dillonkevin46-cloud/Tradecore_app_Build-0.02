from django.db import models
from django.utils import timezone

# 1. CATEGORY MODEL
class MonitorCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-server', help_text="FontAwesome class (e.g. fas fa-server)")

    class Meta:
        verbose_name_plural = "Monitor Categories"

    def __str__(self):
        return self.name

# 2. DEVICE MODEL
class NetworkTarget(models.Model):
    category = models.ForeignKey(MonitorCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, help_text="Device Name (e.g. Primary Server)")
    host = models.CharField(max_length=100, help_text="IP Address or Hostname")
    is_active = models.BooleanField(default=True)
    
    # Status Fields
    is_online = models.BooleanField(default=False)
    # Ensure this is 'last_checked'
    last_checked = models.DateTimeField(null=True, blank=True) 
    response_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.host})"

# 3. DAILY CHECKLIST MODEL
class DailyChecklist(models.Model):
    name = models.CharField(max_length=200, help_text="Task name, e.g. 'Check Backups'")
    is_checked = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 4. SYSTEM SETTINGS
class SystemSetting(models.Model):
    report_email = models.EmailField(help_text="Email address to receive daily reports", default="admin@example.com")
    
    def save(self, *args, **kwargs):
        self.pk = 1 
        super().save(*args, **kwargs)

    def __str__(self):
        return "System Configuration"