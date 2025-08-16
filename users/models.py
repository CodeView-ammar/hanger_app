from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('laundry_owner', 'Laundry Owner'),
        ('carriers', 'Carriers'),
    ]
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_laundry_owner = models.BooleanField(default=False)
    name = models.CharField(max_length=200, blank=True)
    fcm = models.CharField(max_length=200, blank=True)
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='custom_user_set',  # Change this to something unique
    #     blank=True,
    # )
    
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='custom_user_set',  # Change this to something unique
    #     blank=True,
    # )

    def __str__(self):
        return self.name
    
class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    x_map = models.CharField(max_length=100)
    y_map = models.CharField(max_length=100)
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = _("Address")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("Addresss")  # ترجمة الجمع

    def __str__(self):
        return f'Address for {self.user.username}'
    


class Wallet(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # المستخدم المرتبط
    owner_name = models.CharField(max_length=100)  # اسم المالك
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # الرصيد الحالي
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    updated_at = models.DateTimeField(auto_now=True)  # تاريخ التحديث
    status = models.CharField(max_length=20, choices=[('active', 'نشطة'), ('closed', 'مغلقة')])  # حالة المحفظة
    notes = models.TextField(blank=True, null=True)  # ملاحظات
    class Meta:
        verbose_name = _("Wallet")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("Wallets")  # ترجمة الجمع

    def __str__(self):
        return f"{self.owner_name} - {self.balance}"

@receiver(post_save, sender=Users)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:  # تحقق مما إذا كان المستخدم جديدًا
        Wallet.objects.create(user=instance, owner_name=instance.username,
        balance=0,status='active',notes='')  # إنشاء محفظة جديدة

class TransferRequest(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # المناديب
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ
    date_requested = models.DateTimeField(auto_now_add=True)  # تاريخ الطلب
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')  # حالة الطلب
    notes = models.TextField(blank=True, null=True)  # ملاحظات إضافية
    class Meta:
        verbose_name = _("TransferRequest")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("TransferRequests")  # ترجمة الجمع

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"