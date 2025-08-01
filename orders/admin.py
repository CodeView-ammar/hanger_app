from django.contrib import admin
from .models import LaundryOrder, Order, OrderItem, Cart, PaymentDetail,PaymentMethod,PaymentMethodsDetails
from import_export.admin import ExportMixin, ImportExportModelAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # عدد العناصر الفارغة التي تظهر في النموذج

class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'laundry', 'order_date', 'total_amount', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'laundry', 'order_date')
    search_fields = ('user__username', 'laundry__name', 'id')
    inlines = [OrderItemInline]  # إضافة العناصر كعناصر فرعية


class CartAdmin(ImportExportModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')


class LaundryOrderAdmin(ImportExportModelAdmin):
    list_display = ('laundry', 'order', 'assigned_date','status','profit')  # الحقول التي ستظهر في قائمة العرض
    list_filter = ('laundry', 'order', 'assigned_date','status','profit')  # الفلاتر التي يمكنك استخدامها
    search_fields = ('laundry__name', 'order__id')  # حقول البحث

admin.site.register(LaundryOrder, LaundryOrderAdmin)

# تسجيل النماذج في واجهة الإدارة
admin.site.register(Order, OrderAdmin)
# admin.site.register(Cart, CartAdmin)
admin.site.register(PaymentMethod)
admin.site.register(PaymentDetail)

# admin.site.register(PaymentMethodsDetails)
