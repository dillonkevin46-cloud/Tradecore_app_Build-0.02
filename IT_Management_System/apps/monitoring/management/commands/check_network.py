import time
from django.core.management.base import BaseCommand
from django.utils import timezone  # <--- Added
from ping3 import ping
from apps.monitoring.models import NetworkTarget

class Command(BaseCommand):
    help = 'Pings all active network targets to check status'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Network Monitor... (Press Ctrl+C to stop)")
        
        while True:
            targets = NetworkTarget.objects.filter(is_active=True)
            
            for target in targets:
                try:
                    # Ping the host (IP or DNS)
                    # Returns delay in seconds (e.g. 0.02) or None if timeout
                    delay = ping(target.host, timeout=2) 
                    
                    if delay is not None:
                        # Device is UP
                        if not target.is_online:
                            self.stdout.write(self.style.SUCCESS(f"✅ UP: {target.name} came online"))
                        
                        target.is_online = True
                        target.response_time = delay * 1000 # FIXED: Updated field name
                    else:
                        # Device is DOWN
                        if target.is_online:
                            self.stdout.write(self.style.WARNING(f"❌ DOWN: {target.name} went offline"))
                        
                        target.is_online = False
                        target.response_time = None
                        
                except Exception as e:
                    target.is_online = False
                    self.stdout.write(self.style.ERROR(f"ERROR: {target.name} ({target.host}) - {e}"))
                
                # FIXED: Update the timestamp
                target.last_checked = timezone.now()
                target.save()
            
            # Wait 30 seconds before next scan
            time.sleep(30)