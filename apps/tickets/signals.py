from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HRRequest, Ticket
from django.utils import timezone

@receiver(post_save, sender=HRRequest)
def create_onboarding_ticket(sender, instance, created, **kwargs):
    # Only run this if it's a NEW request
    if created:
        Ticket.objects.create(
            title=f"Onboarding: {instance.full_name}",
            description=f"New User Setup.\nRole: {instance.job_title}\nDept: {instance.department}\nStart Date: {instance.start_date}\n\nPlease prepare equipment and accounts.",
            priority='HIGH',
            status='OPEN',
            due_date=timezone.now() # You can adjust this to be instance.start_date if you prefer
        )