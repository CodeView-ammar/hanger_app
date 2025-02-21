from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read', 'status')  # الحقول التي تريد عرضها في القائمة
    list_filter = ('is_read', 'status')  # خيارات الفلترة
    search_fields = ('message',)  # حقول البحث

# تسجيل نموذج الإشعارات في لوحة الإدارة
admin.site.register(Notification, NotificationAdmin)