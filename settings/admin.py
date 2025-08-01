from django.contrib import admin
from .models import Setting ,AppSettings, AppVersion, OTPAPI
from import_export.admin import ExportMixin, ImportExportModelAdmin
@admin.register(Setting)
class SettingAdmin(ImportExportModelAdmin):
    list_display = ('key', 'sales_percentage', 'tax_rate','price_per_kg','price_per_kg_delivery')  # الحقول التي تريد عرضها في قائمة الإعدادات
    search_fields = ('key',)  # يمكن البحث باستخدام المفتاح
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)

        # أخفِ النموذج تمامًا من القائمة الجانبية إذا لم يكن المستخدم مديرًا للمدرسة
        if request.user.role == 'laundry_owner':
            return {}
        return perms
    def has_add_permission(self, request):
        # Disable the add permission
        return False

    def has_delete_permission(self, request, obj=None):
        # Optionally disable delete permission as well
        return False


from .models import SlideShowImage

@admin.register(SlideShowImage)
class SlideShowImageAdmin(ImportExportModelAdmin):
    list_display = ('caption', 'order', 'created_at', 'updated_at')
    ordering = ('order',)


@admin.register(AppVersion)
class AppVersionAdmin(ImportExportModelAdmin):
    list_display = ("platform","type_app","version","force_update","message")
    ordering = ('version',)

admin.site.register(AppSettings)
admin.site.register(OTPAPI)