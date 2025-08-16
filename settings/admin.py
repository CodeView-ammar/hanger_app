from django.contrib import admin
from .models import Setting ,AppSettings, AppVersion, OTPAPI
from import_export.admin import ExportMixin, ImportExportModelAdmin
@admin.register(Setting)
class SettingAdmin(ImportExportModelAdmin):
    list_display = ('key', 'sales_percentage', 'tax_rate','price_per_kg','price_per_kg_delivery')  # الحقول التي تريد عرضها في قائمة الإعدادات
    search_fields = ('key',)  # يمكن البحث باستخدام المفتاح
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


from .models import SlideShowImage

@admin.register(SlideShowImage)
class SlideShowImageAdmin(ImportExportModelAdmin):
    list_display = ('caption', 'order', 'created_at', 'updated_at')
    ordering = ('order',)
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


@admin.register(AppVersion)
class AppVersionAdmin(ImportExportModelAdmin):
    list_display = ("platform","type_app","version","force_update","message")
    ordering = ('version',)
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

@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

@admin.register(OTPAPI)
class OTPAPIAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)
