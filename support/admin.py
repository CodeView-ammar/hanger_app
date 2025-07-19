from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import SupportTicket, SupportMessage, SupportFAQ
from import_export.admin import ExportMixin, ImportExportModelAdmin

class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0
    readonly_fields = ('sender', 'message_type', 'created_at', 'is_read')
    fields = ('sender', 'message_type', 'content', 'attachment', 'created_at', 'is_read')
    
    def has_add_permission(self, request, obj=None):
        return True


@admin.register(SupportTicket)
class SupportTicketAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'title', 'user', 'category', 'priority', 'status', 
        'assigned_to', 'created_at', 'messages_count', 'quick_reply'
    ]
    list_filter = ['status', 'priority', 'category', 'created_at', 'assigned_to']
    search_fields = ['title', 'user__username', 'user__name']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    inlines = [SupportMessageInline]
    
    fieldsets = (
        ('معلومات التذكرة', {
            'fields': ('user', 'title', 'category')
        }),
        ('حالة التذكرة', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def messages_count(self, obj):
        return obj.messages.count()
    messages_count.short_description = 'عدد الرسائل'
    
    def quick_reply(self, obj):
        if obj.status not in ['closed', 'resolved']:
            url = reverse('admin:support_supportmessage_add') + f'?ticket={obj.id}'
            return format_html(
                '<a href="{}" class="button">رد سريع</a>',
                url
            )
        return '-'
    quick_reply.short_description = 'إجراءات'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status in ['resolved', 'closed'] and not obj.resolved_at:
                obj.resolved_at = timezone.now()
        
        super().save_model(request, obj, form, change)
        
        # إضافة رسالة نظام عند تغيير الحالة
        if change and 'status' in form.changed_data:
            SupportMessage.objects.create(
                ticket=obj,
                sender=request.user,
                message_type='system',
                content=f'تم تغيير حالة التذكرة إلى: {obj.get_status_display()}'
            )


@admin.register(SupportMessage)
class SupportMessageAdmin(ImportExportModelAdmin):
    list_display = ['id', 'ticket', 'sender', 'message_type', 'content_preview', 'created_at', 'is_read']
    list_filter = ['message_type', 'created_at', 'is_read']
    search_fields = ['content', 'ticket__title', 'sender__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات الرسالة', {
            'fields': ('ticket', 'sender', 'message_type')
        }),
        ('المحتوى', {
            'fields': ('content', 'attachment')
        }),
        ('معلومات إضافية', {
            'fields': ('created_at', 'is_read'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'معاينة المحتوى'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # تعيين المرسل الحالي كافتراضي
        if not obj:
            form.base_fields['sender'].initial = request.user
            form.base_fields['message_type'].initial = 'support'
        
        return form


@admin.register(SupportFAQ)
class SupportFAQAdmin(ImportExportModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'category']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('السؤال والإجابة', {
            'fields': ('question', 'answer')
        }),
        ('التصنيف والترتيب', {
            'fields': ('category', 'order', 'is_active')
        }),
    )