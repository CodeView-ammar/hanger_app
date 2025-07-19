from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from notification.views import send_order_status_notification


@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    """تتبع تغيير حالة الطلب لإرسال الإشعارات"""
    if instance.pk:  # إذا كان الطلب موجود (تحديث وليس إنشاء)
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            # حفظ الحالة القديمة للمقارنة
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    """إرسال إشعار عند تغيير حالة الطلب"""
    if created:
        # إشعار عند إنشاء طلب جديد
        send_order_status_notification(instance.user, instance, 'pending')
    else:
        # إشعار عند تغيير الحالة
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            send_order_status_notification(instance.user, instance, instance.status)