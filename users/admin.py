from django.contrib import admin
from .models import Users, Address
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users  # Adjust the import based on your app structure
from import_export.admin import ExportMixin, ImportExportModelAdmin
class AddressAdmin(ImportExportModelAdmin):
    list_display = ('user', 'address_line', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    list_filter = ('city', 'state', 'country')
    search_fields = ('user__username', 'address_line', 'city', 'postal_code')

# تسجيل النماذج في واجهة الإدارة
# admin.site.register(Users, UserAdmin)
admin.site.register(Address, AddressAdmin)





@admin.register(Users)
class UsersAdmin(BaseUserAdmin,ImportExportModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('المعلومات الشخصية', {'fields': ('name', 'email', 'phone', 'role', 'is_laundry_owner','fcm')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ مهمة', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'email', 'phone', 'role'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_superuser')
    search_fields = ('username', 'email', 'name', 'phone')
    ordering = ('username',)
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        # إخفاء صفحة المستخدمين من أصحاب المغاسل
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return {}
        return perms
# Register the custom user model with the customized admin


from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from .models import TransferRequest
from accounts.models import  Transaction



@admin.register(TransferRequest)
class TransferRequestAdmin(ImportExportModelAdmin):
    list_display = ('user', 'amount', 'date_requested',"notes", 'status', 'transfer_button')
    list_filter = ('status', 'date_requested')  # إضافة الفلترة حسب الحالة والتاريخ
    search_fields = ('user__username', 'amount')
    ordering = ('-date_requested',)
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        # إخفاء طلبات التحويل من أصحاب المغاسل
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return {}
        return perms

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('transfer/<int:request_id>/', self.admin_site.admin_view(self.process_transfer), name='process_transfer'),
        ]
        return custom_urls + urls

    def process_transfer(self, request, request_id):
        transfer_request = self.get_object(request, request_id)

        if transfer_request is None:
            messages.error(request, "طلب التحويل غير موجود.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if transfer_request.status != 'pending':
            messages.error(request, "طلب التحويل ليس في حالة جاهزة للتحويل.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        transfer_amount = transfer_request.amount

        # إنشاء سجل جديد في جدول Transaction
        Transaction.objects.create(
            user=transfer_request.user,
            transaction_type='transfer',
            amount=transfer_amount,
            debit=0,
            credit=transfer_amount,
            description=f"تحويل مبلغ {transfer_amount} من طلب التحويل."
        )

        # حذف سند الصرف المرتبط إذا كان موجوداً
        try:
            transaction = Transaction.objects.get(
                user=transfer_request.user,
                transaction_type='payment_voucher',
                amount=transfer_amount
            )
            transaction.delete()  # حذف السند
            messages.success(request, "تم حذف سند الصرف بنجاح.")
        except Transaction.DoesNotExist:
            messages.warning(request, "لم يتم العثور على سند الصرف المطلوب.")

        # تحديث حالة الطلب إلى "completed"
        transfer_request.status = 'completed'
        transfer_request.save()

        messages.success(request, "تم تحويل المبلغ بنجاح.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def transfer_button(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" style="background-color:#28a745; color:white; padding:4px 8px; border-radius:4px;" href="{}">صرف</a>',
                reverse('admin:process_transfer', args=[obj.id])
            )
        return "-"

    transfer_button.short_description = 'صرف'
        # منع إضافة طلبات جديدة
    def has_add_permission(self, request):
        return False

    # منع تعديل الطلبات
    def has_change_permission(self, request, obj=None):
        return False
