from django.db import models
from users.models import Users,Wallet
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('receipt_voucher', _('سند قبض')),  # إضافة سند قبض
        ('payment_voucher',  _('سند صرف')),  # إضافة سند صرف
        ('deposit',  _('إيداع')),
        ('withdraw',  _('سحب')),
        # ('transfer',  _('تحويل')),
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
    malaq_ratio = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # حقل الدائن
    description = models.TextField()                             # وصف العملية
    class Meta:
        verbose_name = _("Transaction")  # ترجمة كلمة "Transaction"
        verbose_name_plural = _("Transactions")  # ترجمة الجمع
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username}"

from django.db.models.signals import post_save
from django.dispatch import receiver

from decimal import Decimal

@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    if created:  # تحقق مما إذا كانت العملية قد أنشئت
        wallet = Wallet.objects.get(user=instance.user)

        # تحويل instance.amount إلى Decimal لضمان العمليات الحسابية الصحيحة
        amount = Decimal(instance.amount)

        if instance.transaction_type == 'receipt_voucher':
            wallet.balance += amount  # إضافة المبلغ إلى الرصيد
        elif instance.transaction_type == 'payment_voucher':
            wallet.balance -= amount  # خصم المبلغ من الرصيد
        elif instance.transaction_type == 'deposit':
            wallet.balance += amount  # إضافة المبلغ إلى الرصيد
        elif instance.transaction_type == 'withdraw':
            wallet.balance -= amount  # خصم المبلغ من الرصيد
        # elif instance.transaction_type == 'transfer':
        #     # في حالة التحويل، يمكن أن تتطلب من حسابين
        #     # تحتاج إلى منطق إضافي هنا
        #     pass
        elif instance.transaction_type == 'bill_payment':
            wallet.balance -= amount  # خصم المبلغ من الرصيد
        elif instance.transaction_type == 'refund':
            wallet.balance += amount  # إضافة المبلغ إلى الرصيد

        wallet.save()  # حفظ التغييرات في المحفظة

class Statistics(models.Model):
    laundries_count = models.PositiveIntegerField(default=0)  # عدد المغاسل
    agents_count = models.PositiveIntegerField(default=0)      # عدد المناديب
    updated_at = models.DateTimeField(auto_now=True)          # تاريخ آخر تحديث

    def __str__(self):
        return f"Statistics: {self.laundries_count} laundries, {self.agents_count} agents"