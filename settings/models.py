from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Setting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    sales_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # حقل جديد لنسبة الضريبة
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر الكيلو
    price_per_kg_delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر الكيلو للمندوب
    
    class Meta:
        verbose_name = _("Setting")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("Settings")  # ترجمة الجمع




class SlideShowImage(models.Model):
    image = models.ImageField(upload_to='slideshow_images/')  # مسار حفظ الصور
    caption = models.CharField(max_length=255, blank=True, null=True)  # عنوان الصورة
    order = models.PositiveIntegerField(default=0)  # ترتيب الصورة في السلايد شو
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    updated_at = models.DateTimeField(auto_now=True)  # تاريخ التحديث

    class Meta:
        ordering = ['order']  # ترتيب الصور حسب حقل order
        verbose_name = _("SlideShowImage")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("SlideShowImages")  # ترجمة الجمع

    def __str__(self):
        return self.caption if self.caption else f"Image {self.id}"





class AppSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    class Meta:
        verbose_name = _("AppSettings")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("AppSettings")  # ترجمة الجمع

    def __str__(self):
        return self.key


class AppVersion(models.Model):
    PLATFORM_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web'),
    ]
    APP_CHOICES = [
        ('hangeragent', 'وكيل معلاق'),
        ('hangermain', 'ملاق الرئيسي'),
    ]
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    type_app = models.CharField(max_length=20, choices=APP_CHOICES)
    version = models.CharField(max_length=20, unique=True)
    force_update = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    class Meta:
        verbose_name = _("AppVersion")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("AppVersions")  # ترجمة الجمع

    def __str__(self):
        return f"{self.platform} - {self.version}"

class OTPAPI(models.Model):
    phone_number = models.CharField(max_length=15)  # يمكن تعديل الطول حسب الحاجة
    otp_code = models.CharField(max_length=6)  # طول رمز OTP
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    class Meta:
        verbose_name = _("OTPAPI")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("OTPAPIs")  # ترجمة الجمع

    def __str__(self):
        return f"{self.phone_number} - {self.otp_code}"

