from django.db import models
from users.models import Users  # Ensure to import your Users model
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# from orders.models import Order
def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB limit
    if value.size > max_size:
        raise ValidationError(f"File size should not exceed {max_size / (1024 * 1024)} MB.")

class SalesAgent(models.Model):
    CITY_CHOICES = [
        ('riyadh', 'الرياض'),
        ('dammam', 'الدمام'),
        ('jeddah', 'جدة'),
        ('khobar', 'الخبر'),
        ('mecca', 'مكة المكرمة'),
        ('medina', 'المدينة المنورة'),
    ]
    VEHICLE_TYPE_CHOICES = [
        ('car', 'سيارة'),
        ('motorcycle', 'دراجة نارية'),
        ('bicycle', 'دراجة هوائية'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)  # رقم الهوية
    id_image = models.FileField(upload_to='id_images/', validators=[validate_file_size])  # صورة الهوية
    license_number = models.CharField(max_length=20)  # رقم الرخصة
    license_image = models.FileField(upload_to='license_images/', validators=[validate_file_size])  # صورة الرخصة
    city = models.CharField(max_length=20, choices=CITY_CHOICES)  # المدينة
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)  # نوع السيارة
    	
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sales_agent2')  # إضافة حقل user

    def save(self, *args, **kwargs):
        # Resize and save id_image
        if self.id_image:
            img = Image.open(self.id_image)
            img = img.resize((1024, 1024), Image.LANCZOS)  # Use LANCZOS for high-quality resizing
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')  # Save as JPEG
            img_file = ContentFile(img_io.getvalue(), name=self.id_image.name)
            self.id_image = img_file  # Assign resized image to id_image field

        # Optionally, handle license_image resizing here as well
        if self.license_image:
            img = Image.open(self.license_image)
            img = img.resize((1024, 1024), Image.LANCZOS)  # Use LANCZOS for high-quality resizing
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')  # Save as JPEG
            img_file = ContentFile(img_io.getvalue(), name=self.license_image.name)
            self.license_image = img_file  # Assign resized image to license_image field

        # Create a new user only if this is a new SalesAgent instance
        if not self.pk:  # Check if the instance is new
            user = Users(
                name=self.name,
                username=self.phone,  # Use phone as username
                email=self.email,
                phone=self.phone,
                role='carriers',  # Set the appropriate role
                password=self.phone,  # Use phone as password (consider hashing it)
                is_active=False,  # Set to inactive initially
            )
            user.save()  # Save the new user
            self.user = user  # Set the user field

        super().save(*args, **kwargs)  # Save the SalesAgent instance
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _("SalesAgent")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("SalesAgents")  # ترجمة الجمع