from django.db import models
from agent.models import SalesAgent
from users.models import Users
from laundries.models import Laundry
from services.models import Service
from django.utils import timezone

class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'الدفع عند الاستلام'),  # Cash on Delivery
        ('CARD', 'الدفع باستخدام البطاقة'),  # Card Payment
        ('STC', 'الدفع باستخدام STC'),  # STC Payment
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=PAYMENT_CHOICES, unique=True) 
    description = models.TextField(blank=True, null=True)  # وصف طريقة الدفع (اختياري)
    is_active = models.BooleanField(default=True)  # حالة تفعيل طريقة الدفع
    default = models.BooleanField(default=False) 
    def __str__(self):
        return self.name


class PaymentMethodsDetails(models.Model):
    payment_method = models.OneToOneField(PaymentMethod,on_delete=models.CASCADE)
    card_name = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    card_expiry_date = models.CharField(max_length=20, null=True, blank=True)
    cvv = models.CharField(max_length=4, null=True, blank=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('courier_accepted', 'التسليم للمندوب'),
        ('courier_on_the_way', 'المندوب في الطريق'),
        ('picked_up_from_customer', 'تم اخذها من العميل'),
        ('delivered_to_laundry', 'تم التسليم للمغسلة'),
        ('in_progress', 'الطلب قيد المعالجة'),
        ('ready_for_delivery', 'جاهز للتسليم'),
     
    
        # بعد الانتهاء من الغسيل 
        ('delivery_by_courier', 'التوصيل عن طريق المندوب'), 
        ('courier_accepted_delivery', 'المندوب قبل طلب التوصيل'), 

        ('delivered_to_customer',"تم تسليم الطلب للعميل"),
        ('delivered_to_courier',"تم تسليم الطلب للمندوب"),

        ('completed', 'مكتمل'),
        ('canceled', 'تم الإلغاء'), 
    ]
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    pickup_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'),('unpaid', 'Unpaid'),], default='unpaid')
    payment_method= models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    sales_agent = models.ForeignKey(SalesAgent, on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    

class OrderItem(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('normal', 'عادي'),
        ('urgent', 'مستعجل'),
    ]

    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)  # نوع الخدمة
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(blank=True, null=True,max_length=1000,)

    def __str__(self):
        return f'Item {self.service.name} in Order {self.order.id}'
    

class Cart(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('normal', 'عادي'),
        ('urgent', 'مستعجل'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    urgent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # سعر مستعجل
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES,default='normal')  # نوع الخدمة
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'laundry', 'service')  # قيد فريد

    def __str__(self):
        return f'Cart for {self.user.username}'


class LaundryOrder(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
     
    status = models.CharField(max_length=255)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # حقل أرباح التوصيل

    class Meta:
        # unique_together = ('sales_agent', 'order')  # لضمان عدم تكرار العلاقة
        verbose_name = 'laundry Order'
        verbose_name_plural = 'laundry Orders'

    def __str__(self):
        return f'Order {self.order.id} assigned to {self.laundry.name}'

class PaymentDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_details')
    payment_date = models.DateTimeField(auto_now_add=True)  # تاريخ الدفع
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ المدفوع
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)  # طريقة الدفع
    transaction_id = models.CharField(max_length=255, unique=True)  # معرف المعاملة
    status = models.CharField(max_length=10, choices=[
        ('successful', 'ناجح'),
        ('failed', 'فاشل'),
        ('pending', 'قيد الانتظار'),
    ], default='pending')  # حالة الدفع
    note=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f'Payment {self.transaction_id} for Order {self.order.id}'


class SalesAgentOrder(models.Model):
    sales_agent = models.ForeignKey(SalesAgent, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    delivery_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # حقل أرباح التوصيل

    class Meta:
        # unique_together = ('sales_agent', 'order')  # لضمان عدم تكرار العلاقة
        verbose_name = 'Sales Agent Order'
        verbose_name_plural = 'Sales Agent Orders'

    def __str__(self):
        return f'Order {self.order.id} assigned to {self.sales_agent.name}'