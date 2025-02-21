from django.contrib import admin
from .models import Service,ServiceCategory

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','price', 'duration', 'created_at', 'updated_at')
    list_filter = ('price',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

# تسجيل النموذج في واجهة الإدارة
admin.site.register(Service, ServiceAdmin)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # الحقول التي ستظهر في قائمة الفئات
    search_fields = ('name',)  # البحث حسب الاسم
