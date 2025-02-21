from django.contrib import admin
from .models import ServiceReview

class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating', 'created_at')
    list_filter = ('service', 'rating', 'created_at')
    search_fields = ('user__username', 'service__name', 'comment')
    ordering = ('-created_at',)

# تسجيل النموذج في واجهة الإدارة
admin.site.register(ServiceReview, ServiceReviewAdmin)