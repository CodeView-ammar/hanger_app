from django.db import models
from laundries.models import Laundry



class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # اسم الفئة
    description = models.TextField(blank=True, null=True)  # وصف الفئة

    def __str__(self):
        return self.name
    
class Service(models.Model):

    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True,max_length=1000,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    urgent_price = models.DecimalField(max_digits=10, decimal_places=2)  # سعر مستعجل
    
    duration = models.IntegerField()  # مدة الخدمة بالساعة
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LaundryService(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE, related_name='laundry_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_laundries')
    # custom_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # سعر مخصص لكل مغسلة
    # available = models.BooleanField(default=True)  # حالة الخدمة

    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True,max_length=1000,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    urgent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر مستعجل
    
    duration = models.IntegerField()  # مدة الخدمة بالساعة
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    # category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('laundry', 'service')  # لضمان عدم تكرار العلاقة

    def __str__(self):
        return f"{self.name}"