from django.db import models
from orders.models import Order
from laundries.models import Laundry

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('online', 'Online'),
    ])

    def __str__(self):
        return f'Invoice for Order {self.order.id}'