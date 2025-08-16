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
    inlines = [OrderItemInline]

    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_delete_permission(request, obj)

class CartAdmin(ImportExportModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')

    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_delete_permission(request, obj)

class LaundryOrderAdmin(ImportExportModelAdmin):
    list_display = ('laundry', 'order', 'assigned_date', 'status', 'profit')
    list_filter = ('laundry', 'order', 'assigned_date', 'status', 'profit')
    search_fields = ('laundry__name', 'order__id')

    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_delete_permission(request, obj)

# تسجيل النماذج في واجهة الإدارة
admin.site.register(Order, OrderAdmin)
admin.site.register(LaundryOrder, LaundryOrderAdmin)

# إخفاء طرق الدفع وتفاصيل الدفع عن المستخدمين من نوع laundry_owner
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

# يمكنك التعليق على هذا السطر إذا كنت لا ترغب في استخدامه
# admin.site.register(Cart, CartAdmin)