from django.db.models.signals import post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Callers

@receiver(post_delete, sender=Callers)
def send_data_update_on_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "data_updates",
        {
            "type": "data_update",
            "data": {"number": instance.name},
        },
    )
