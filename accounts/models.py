from django.db import models
from users.models import Users
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('receipt_voucher', _('سند قبض')),  # إضافة سند قبض
        ('payment_voucher',  _('سند صرف')),  # إضافة سند صرف
        ('deposit',  _('إيداع')),
        ('withdraw',  _('سحب')),
        ('transfer',  _('تحويل')),
        ('bill_payment',  _('دفع فواتير')),
        ('refund',  _('استرداد')),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # المستخدم المرتبط
    date = models.DateTimeField(auto_now_add=True)            # تاريخ العملية
    date_jsut = models.DateField(auto_now_add=True)  # تاريخ العملية فقط
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)  # نوع العملية
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # حقل المدين
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # حقل الدائن
    description = models.TextField()                             # وصف العملية

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username}"