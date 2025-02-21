from django.db import models
from django.contrib.auth.models import User

class Setting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    sales_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # حقل جديد لنسبة الضريبة
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر الكيلو
    price_per_kg_delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر الكيلو للمندوب





class SlideShowImage(models.Model):
    image = models.ImageField(upload_to='slideshow_images/')  # مسار حفظ الصور
    caption = models.CharField(max_length=255, blank=True, null=True)  # عنوان الصورة
    order = models.PositiveIntegerField(default=0)  # ترتيب الصورة في السلايد شو
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    updated_at = models.DateTimeField(auto_now=True)  # تاريخ التحديث

    class Meta:
        ordering = ['order']  # ترتيب الصور حسب حقل order

    def __str__(self):
        return self.caption if self.caption else f"Image {self.id}"