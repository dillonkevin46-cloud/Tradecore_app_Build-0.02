from django.apps import AppConfig

class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tickets'  # <--- It must be 'apps.tickets'
    
    # Keep the signals import if you added it earlier
    def ready(self):
        import apps.tickets.signals