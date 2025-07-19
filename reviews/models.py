from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import Users
from services.models import Service
from laundries.models import Laundry


# class ServiceReview(models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Review for {self.service.name} by {self.user.username}'

class LaundryReview(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="تقييم من 1 إلى 5 نجوم"
    )
    comment = models.TextField(blank=True, null=True, help_text="تعليق اختياري")
    service_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        default=5,
        help_text="تقييم جودة الخدمة"
    )
    delivery_speed = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        default=5,
        help_text="تقييم سرعة التوصيل"
    )
    price_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        default=5,
        help_text="تقييم مناسبة السعر"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('laundry', 'user')  # منع المستخدم من تقييم نفس المغسلة أكثر من مرة
        ordering = ['-created_at']

    def __str__(self):
        return f'تقييم {self.laundry.name} بواسطة {self.user.username} - {self.rating} نجوم'

    @property
    def average_rating(self):
        """حساب متوسط التقييم للجوانب المختلفة"""
        return (self.service_quality + self.delivery_speed + self.price_value) / 3
