from django.contrib import admin
from .models import Service,ServiceCategory,LaundryService, SubService
from import_export.admin import ExportMixin, ImportExportModelAdmin


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('name','price', 'duration',"category", 'created_at', 'updated_at')
    list_filter = ('price',)
    search_fields = ('name', 'description',"category")
    ordering = ('-created_at',)

# تسجيل النموذج في واجهة الإدارة
admin.site.register(Service, ServiceAdmin)
# admin.site.register(LaundryService)
@admin.register(LaundryService)
class LaundryServiceAdmin(ImportExportModelAdmin):
    pass

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description')  # الحقول التي ستظهر في قائمة الفئات
    search_fields = ('name',)  # البحث حسب الاسم


admin.site.register(SubService)
