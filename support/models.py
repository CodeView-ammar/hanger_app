from django.db import models
from users.models import Users


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'مفتوح'),
        ('in_progress', 'قيد المعالجة'),
        ('resolved', 'محلول'),
        ('closed', 'مغلق'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'منخفض'),
        ('medium', 'متوسط'),
        ('high', 'عالي'),
        ('urgent', 'عاجل'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'استفسار عام'),
        ('technical', 'مشكلة تقنية'),
        ('billing', 'مشكلة فواتير'),
        ('order', 'مشكلة طلب'),
        ('complaint', 'شكوى'),
        ('suggestion', 'اقتراح'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=200, verbose_name='عنوان التذكرة')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', verbose_name='التصنيف')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='الأولوية')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open', verbose_name='الحالة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ الحل')
    assigned_to = models.ForeignKey(
        Users, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets',
        limit_choices_to={'is_staff': True},
        verbose_name='مُسند إلى'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تذكرة دعم فني'
        verbose_name_plural = 'تذاكر الدعم الفني'

    def __str__(self):
        return f'#{self.id} - {self.title} ({self.user.username})'


class SupportMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('user', 'رسالة من المستخدم'),
        ('support', 'رسالة من الدعم الفني'),
        ('system', 'رسالة نظام'),
    ]

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='المرسل')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, verbose_name='نوع الرسالة')
    content = models.TextField(verbose_name='محتوى الرسالة')
    attachment = models.FileField(upload_to='support_attachments/', null=True, blank=True, verbose_name='مرفق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')
    is_read = models.BooleanField(default=False, verbose_name='مقروءة')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'رسالة دعم فني'
        verbose_name_plural = 'رسائل الدعم الفني'

    def __str__(self):
        return f'رسالة في التذكرة #{self.ticket.id} من {self.sender.username}'


class SupportFAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name='السؤال')
    answer = models.TextField(verbose_name='الإجابة')
    category = models.CharField(max_length=50, verbose_name='التصنيف')
    order = models.PositiveIntegerField(default=0, verbose_name='الترتيب')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'سؤال شائع'
        verbose_name_plural = 'الأسئلة الشائعة'

    def __str__(self):
        return self.question