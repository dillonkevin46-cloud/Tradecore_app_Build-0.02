from django.db import models
from apps.monitoring.models import MonitorCategory

# 1. NEW: Asset Categories (e.g. Laptops, Vehicles, Tools)
class AssetCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Asset Categories"

    def __str__(self):
        return self.name

# 2. UPDATED: Asset Model
class Asset(models.Model):
    # Core Info
    device_name = models.CharField(max_length=100)
    # New Link to Category
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Specs
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    cpu = models.CharField(max_length=50, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    storage = models.CharField(max_length=50, blank=True)
    
    # Location
    site = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Network
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    # Integration
    is_monitored = models.BooleanField(default=False)
    monitor_category = models.ForeignKey(
        MonitorCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Select which group this device belongs to in the Network Monitor."
    )
    
    # Meta
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_name} - {self.serial_number}"