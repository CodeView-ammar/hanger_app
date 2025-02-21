from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'invoice_date', 'total_amount', 'status', 'payment_method')
    list_filter = ('status', 'payment_method', 'invoice_date')
    search_fields = ('order__id',)
    ordering = ('-invoice_date',)

# تسجيل النموذج في واجهة الإدارة
admin.site.register(Invoice, InvoiceAdmin)