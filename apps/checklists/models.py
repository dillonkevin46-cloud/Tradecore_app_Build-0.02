from django.db import models
from django.contrib.auth.models import User

# 1. The Questions (e.g. "Check Backups")
class ChecklistItem(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# 2. The Daily Report Wrapper (e.g. "Report for Jan 07")
class DailyReport(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report {self.date} by {self.technician}"

# 3. The Specific Answers (e.g. "Backups = PASS")
class ReportEntry(models.Model):
    report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='entries')
    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('PASS', 'Pass'),
        ('WARNING', 'Warning'),
        ('FAIL', 'Fail'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.item.name}: {self.status}"

# 4. Email Recipients (Indentation Fixed Here)
class ReportRecipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"