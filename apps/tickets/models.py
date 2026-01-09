from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. NEW: Categories (Managed in Admin)
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Choices for dropdowns
PRIORITY_CHOICES = [
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High - Urgent'),
    ('CRITICAL', 'Critical - System Down'),
]

STATUS_CHOICES = [
    ('OPEN', 'Open'),
    ('IN_PROGRESS', 'In Progress'),
    ('WAITING', 'Waiting on User'),
    ('RESOLVED', 'Resolved'),
    ('CLOSED', 'Closed'),
]

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    # Link to Category (Optional, set to null if category deleted)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.title}"

# 2. NEW: Comments Logic
class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on #{self.ticket.id}"

# HR Request (Kept same as before)
class HRRequest(models.Model):
    full_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    start_date = models.DateField()
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)