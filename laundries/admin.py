from django.contrib import admin
from services.models import Service
from users.models import Address
from .models import Laundry, LaundryHours, UserLaundryMark, Users
from import_export.admin import ExportMixin, ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# ======= Laundry Admin =======
class LaundryHoursInline(admin.TabularInline):
    model = LaundryHours
    extra = 1

@admin.register(Laundry)
class LaundryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'address', 'phone', 'email', 'created_at', 'updated_at','owner_id')
    inlines = [LaundryHoursInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return qs.filter(owner=request.user)
        return qs

    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return True
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return True
        return True

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if obj is None:
                return True
            return obj.owner == request.user
        return True

    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return not Laundry.objects.filter(owner=request.user).exists()
        return True

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if obj is None:
                return True
            return obj.owner == request.user
        return True

# ======= Service Admin =======
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price', 'duration', "category", 'created_at', 'updated_at')
    list_filter = ('price',)
    search_fields = ('name', 'description', "category")
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if hasattr(request.user, 'laundry'):
                return qs.filter(laundry=request.user.laundry)
            else:
                return qs.none()
        return qs

    def has_module_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return True
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

# ======= Users Admin =======
try:
    admin.site.unregister(Users)
except admin.sites.NotRegistered:
    pass
@admin.register(Users)
class UsersAdmin(BaseUserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('المعلومات الشخصية', {'fields': ('name',)}),  # فقط الاسم قابل للتعديل
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

    # عرض بيانات المستخدم نفسه فقط إذا كان صاحب مغسلة
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return qs.filter(pk=request.user.pk)
        return qs

    # السماح بتعديل بياناته فقط
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            if obj is None:
                return True
            return obj.pk == request.user.pk
        return True

    # منع الإضافة والحذف لصاحب المغسلة
    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return False
        return True

    # جعل باقي الحقول غير قابلة للتعديل لصاحب المغسلة (ما عدا الاسم وكلمة المرور)
    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return ('email', 'phone', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined')
        return super().get_readonly_fields(request, obj)

# ======= Address Admin =======
class AddressAdmin(ImportExportModelAdmin):
    list_display = ('user', 'address_line', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    list_filter = ('city', 'state', 'country')
    search_fields = ('user__username', 'address_line', 'city', 'postal_code')

admin.site.register(Address, AddressAdmin)
