from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import Notification
from users.models import Users


# فورم مخصص لإدخال نص الإشعار ونوعه
class BroadcastNotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="نص الإشعار")
    status = forms.ChoiceField(choices=Notification.STATUS_CHOICES, label="نوع الإشعار")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read', 'status')
    list_filter = ('is_read', 'status')
    search_fields = ('message', 'user__username')
    change_list_template = "admin/notifications_changelist.html"  # قوالب مخصصة

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-broadcast/', self.admin_site.admin_view(self.send_broadcast_view), name='send_broadcast'),
        ]
        return custom_urls + urls

    def send_broadcast_view(self, request):
        if request.method == 'POST':
            form = BroadcastNotificationForm(request.POST)
            if form.is_valid():
                message_text = form.cleaned_data['message']
                status = form.cleaned_data['status']
                users = Users.objects.filter(is_active=True)

                for user in users:
                    Notification.objects.create(
                        user=user,
                        message=message_text,
                        status=status
                    )
                self.message_user(request, f"تم إرسال الإشعار إلى {users.count()} مستخدم.", messages.SUCCESS)
                return redirect("..")
        else:
            form = BroadcastNotificationForm()

        context = dict(
            self.admin_site.each_context(request),
            title="إرسال إشعار جماعي",
            form=form,
        )
        return render(request, "admin/send_broadcast.html", context)


        # إخفاء الموديل عن المستخدم من نوع laundry_owner
    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return super().has_delete_permission(request, obj)
