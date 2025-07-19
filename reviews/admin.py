from django.contrib import admin
from .models import LaundryReview
from import_export.admin import ExportMixin, ImportExportModelAdmin
class LaundryReviewAdmin(ImportExportModelAdmin):
    list_display = ('laundry', 'user', 'rating', 'service_quality', 'delivery_speed', 'price_value', 'average_rating', 'created_at')
    list_filter = ('laundry', 'rating', 'service_quality', 'delivery_speed', 'price_value', 'created_at')
    search_fields = ('user__username', 'laundry__name', 'comment')
    ordering = ('-created_at',)
    
    def average_rating(self, obj):
        return round(obj.average_rating, 2)
    average_rating.short_description = 'متوسط التقييم'

admin.site.register(LaundryReview, LaundryReviewAdmin)
