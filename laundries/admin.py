from django.contrib import admin

from services.models import Service
from .models import Laundry
from .models import Laundry, LaundryHours,UserLaundryMark
from import_export.admin import ExportMixin, ImportExportModelAdmin

class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price', 'duration', "category", 'created_at', 'updated_at')
    list_filter = ('price',)
    search_fields = ('name', 'description', "category")
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # عرض فقط الخدمات المرتبطة بالمغسلة الخاصة بالمستخدم إذا كان laundry_owner
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if hasattr(request.user, 'laundry'):
                return qs.filter(laundry=request.user.laundry)
            else:
                return qs.none()
        return qs  # المشرف أو غيره يرى كل شيء

    def has_module_permission(self, request):
        return request.user.is_superuser or (
            hasattr(request.user, 'role') and request.user.role == 'laundry_owner'
        )

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)
