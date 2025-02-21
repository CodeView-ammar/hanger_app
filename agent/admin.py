from django.contrib import admin

from orders.models import SalesAgentOrder
from .models import SalesAgent

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'region', 'id_number', 'license_number', 'city', 'created_at','user_id')
    search_fields = ('name', 'phone', 'email', 'id_number', 'license_number')
    list_filter = ('city',)

    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'region', 'id_number', 'id_image', 'license_number', 'license_image', 'city','user')
        }),
    )
class SalesAgentOrderAdmin(admin.ModelAdmin):
    list_display = ('sales_agent', 'order', 'assigned_date','status','delivery_profit')  # الحقول التي ستظهر في قائمة العرض
    list_filter = ('sales_agent', 'order', 'assigned_date','status','delivery_profit')  # الفلاتر التي يمكنك استخدامها
    search_fields = ('sales_agent__name', 'order__id')  # حقول البحث

admin.site.register(SalesAgentOrder, SalesAgentOrderAdmin)