from django.contrib import admin

from orders.models import SalesAgentOrder
from .models import SalesAgent
from import_export.admin import ExportMixin, ImportExportModelAdmin

@admin.register(SalesAgent)
class SalesAgentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'phone', 'email', 'region', 'id_number', 'license_number', 'city', 'created_at','user_id')
    search_fields = ('name', 'phone', 'email', 'id_number', 'license_number')
    list_filter = ('city',)

    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'region', 'id_number', 'id_image', 'license_number', 'license_image', 'city','user')
        }),
    )

    # إخفاء الموديل عن المستخدم من نوع laundry_owner
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

class SalesAgentOrderAdmin(ImportExportModelAdmin):
    list_display = ('sales_agent', 'order', 'assigned_date','status','delivery_profit')  # الحقول التي ستظهر في قائمة العرض
    list_filter = ('sales_agent', 'order', 'assigned_date','status','delivery_profit')  # الفلاتر التي يمكنك استخدامها
    search_fields = ('sales_agent__name', 'order__id')  # حقول البحث
        # إخفاء الموديل عن المستخدم من نوع laundry_owner
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

admin.site.register(SalesAgentOrder, SalesAgentOrderAdmin)