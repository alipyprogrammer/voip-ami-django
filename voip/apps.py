from django.apps import AppConfig
# from .models import ActiveChannels

class VoipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voip'
    
    # def ready(self):
    #     import voip.signals