from django.db import models
from users.models import Users
class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # ربط الإشعار بالمستخدم
    message = models.TextField()  # نص الإشعار
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    is_read = models.BooleanField(default=False)  # حالة القراءة

    # تعريف خيارات الحالة
    STATUS_CHOICES = [
        ('error', 'Error'),
        ('alert', 'Alert'),
        ('confirmation', 'Confirmation'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='alert')  # حالة الإشعار

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'