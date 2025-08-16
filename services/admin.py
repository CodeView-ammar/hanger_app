from django.contrib import admin
from .models import Service,ServiceCategory, SubService
from import_export.admin import ExportMixin, ImportExportModelAdmin


class ServiceAdmin(ImportExportModelAdmin):
    list_filter = ('price',)
    search_fields = ('name', 'description', 'category')
    ordering = ('-created_at',)

    def get_list_display(self, request):
        # عرض خانة المغسلة حسب دور المستخدم
        if request.user.role == 'laundry_owner':
            return ('name', 'price', 'duration', 'category', 'created_at', 'updated_at')
        return ('laundry_owner_name','name', 'price', 'duration', 'category', 'created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'laundry_owner':
            laundry = request.user.laundries.first()
            if laundry:
                return qs.filter(laundry=laundry)
            return qs.none()
        return qs

    def laundry_owner_name(self, obj):
        # إرجاع اسم مالك المغسلة
        return obj.laundry.owner_name if obj.laundry else 'غير متوفر'

    laundry_owner_name.short_description = 'اسم المغسلة'  # تعيين عنوان الخانة

# تسجيل النموذج
admin.site.register(Service, ServiceAdmin)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    
admin.site.register(SubService)