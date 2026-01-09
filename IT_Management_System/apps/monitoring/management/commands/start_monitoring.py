import time
import subprocess
import platform
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.monitoring.models import NetworkTarget

class Command(BaseCommand):
    help = 'Starts the infinite loop to ping network devices'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Network Monitor... (Press Ctrl+C to stop)'))
        
        while True:
            targets = NetworkTarget.objects.filter(is_active=True)
            
            for target in targets:
                self.ping_device(target)
            
            # Wait 15 seconds before the next round
            self.stdout.write("Waiting 15 seconds...", ending='\n')
            self.stdout.flush()
            time.sleep(15)

    def ping_device(self, target):
        # Build the command based on OS (Windows uses -n, Linux uses -c)
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # FIXED: Changed target.ip_address to target.host
        command = ['ping', param, '1', target.host]

        try:
            # Run the ping command
            start_time = time.time()
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            end_time = time.time()
            
            is_success = output.returncode == 0
            
            # Update the database
            if is_success:
                latency = round((end_time - start_time) * 1000, 2) # Convert to ms
                target.is_online = True
                # FIXED: Changed latency_ms to response_time
                target.response_time = latency
                self.stdout.write(self.style.SUCCESS(f"✅ {target.name} is ONLINE ({latency}ms)"))
            else:
                target.is_online = False
                target.response_time = 0
                self.stdout.write(self.style.ERROR(f"❌ {target.name} is OFFLINE"))
                
                # Note: DownLog model usage is removed here if you haven't created it yet. 
                # If you have a DownLog model, you can keep the creation logic.

            target.last_checked = timezone.now()
            target.save()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error pinging {target.name}: {e}"))