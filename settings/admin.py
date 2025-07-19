from django.contrib import admin
from .models import Setting  # تأكد من استيراد النموذج
from import_export.admin import ExportMixin, ImportExportModelAdmin
@admin.register(Setting)
class SettingAdmin(ImportExportModelAdmin):
    list_display = ('key', 'sales_percentage', 'tax_rate','price_per_kg','price_per_kg_delivery')  # الحقول التي تريد عرضها في قائمة الإعدادات
    search_fields = ('key',)  # يمكن البحث باستخدام المفتاح

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