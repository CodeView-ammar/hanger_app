from django.db import models
# from orders.models import Ordersss
from users.models import Users
# from services.models import Service
from settings.models import Setting

class Laundry(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='laundries') 
    owner_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    x_map = models.CharField(max_length=100)
    y_map = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.FileField(upload_to='laundry_images/', blank=True, null=True)  # Add Imag
    membership_start_date = models.DateField(null=True, blank=True)  # تاريخ بداية العضوية
    membership_end_date = models.DateField(null=True, blank=True)    # تاريخ نهاية العضوية
    sales_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=None)  # Allow null
    is_hidden = models.BooleanField(default=False)  # حقل إخفاء المغسلة
    is_active = models.BooleanField(default=True)  # حقل إيقاف المغسلة
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # تعيين القيمة الافتراضية من جدول الإعدادات
        if self.sales_percentage is None:  # إذا لم يتم تعيين القيمة
            try:
                setting = Setting.objects.get(key='default_sales_percentage')  # استخدم المفتاح المناسب
                self.sales_percentage = setting.sales_percentage
            except Setting.DoesNotExist:
                self.sales_percentage = self.sales_percentage  # قيمة افتراضية احتياطية
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class LaundryHours(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE, related_name='hours')
    day_of_week = models.CharField(max_length=10, choices=[
        ('saturday', 'السبت'),
        ('sunday', 'الأحد'),
        ('monday', 'الاثنين'),
        ('tuesday', 'الثلاثاء'),
        ('wednesday', 'الأربعاء'),
        ('thursday', 'الخميس'),
        ('friday', 'الجمعة'),
    ])
    opening_time = models.TimeField()  # وقت بداية الدوام
    closing_time = models.TimeField()  # وقت نهاية الدوام

    def __str__(self):
        return f"{self.laundry.name} - {self.day_of_week}"


class UserLaundryMark(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_laundries')
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE, related_name='laundry_users')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'laundry')  # لضمان عدم تكرار العلاقة

    def __str__(self):
        return f"{self.user.username} - {self.laundry.name}"

