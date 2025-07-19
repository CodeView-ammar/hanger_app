from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification_to_websocket(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.user.id}",  # اسم مجموعة المستخدم
            {
                "type": "send_notification",  # يطابق دالة المستهلك consumer
                "message": instance.message,
                "status": instance.status,
                "created_at": instance.created_at.isoformat(),
                "id": instance.id,
                "is_read": instance.is_read,
            }
        )
