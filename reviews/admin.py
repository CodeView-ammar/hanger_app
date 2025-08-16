from django.contrib import admin
from .models import LaundryReview
from import_export.admin import ImportExportModelAdmin

class LaundryReviewAdmin(ImportExportModelAdmin):
    list_display = ('laundry', 'user', 'rating', 'service_quality', 'delivery_speed', 'price_value', 'average_rating', 'created_at')
    list_filter = ('laundry', 'rating', 'service_quality', 'delivery_speed', 'price_value', 'created_at')
    search_fields = ('user__username', 'laundry__name', 'comment')
    ordering = ('-created_at',)

    readonly_fields = ['laundry', 'user', 'rating', 'service_quality', 'delivery_speed', 'price_value', 'comment', 'created_at']

    def average_rating(self, obj):
        return round(obj.average_rating, 2)
    average_rating.short_description = 'متوسط التقييم'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # إظهار فقط تقييمات مغسلته إن كان صاحب مغسلة
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return qs.filter(laundry__owner=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        # لا يسمح لصاحب المغسلة بالتعديل إلا لحقل الرد فقط
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if request.method in ['POST', 'PUT', 'PATCH'] and obj:
                # السماح فقط لو تم تعديل حقل الرد
                allowed_fields = ['owner_reply']
                changed_fields = request.POST.keys()
                return all(field in allowed_fields for field in changed_fields)
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # لا يسمح لصاحب المغسلة بالحذف
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return self.readonly_fields + [f.name for f in self.model._meta.fields if f.name != 'owner_reply']
        return self.readonly_fields

admin.site.register(LaundryReview, LaundryReviewAdmin)
