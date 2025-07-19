from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('laundry_owner', 'Laundry Owner'),
        ('carriers', 'Carriers'),
    ]
    
    # username = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=255)
    # email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_laundry_owner = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
    )

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

    def __str__(self):
        return f"{self.owner_name} - {self.balance}"

@receiver(post_save, sender=Users)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:  # تحقق مما إذا كان المستخدم جديدًا
        Wallet.objects.create(user=instance, owner_name=instance.username,
        balance=0,status='active',notes='')  # إنشاء محفظة جديدة