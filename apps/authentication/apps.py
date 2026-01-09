from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # The default is just 'authentication', which is WRONG for your structure.
    # Change it to:
    name = 'apps.authentication'
