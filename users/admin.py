from django.contrib import admin
from .models import Users, Address

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'phone', 'role', 'is_laundry_owner', 'created_at', 'updated_at')
#     list_filter = ('role', 'is_laundry_owner', 'created_at')
#     search_fields = ('username', 'email', 'phone')
#     ordering = ('-created_at',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    list_filter = ('city', 'state', 'country')
    search_fields = ('user__username', 'address_line', 'city', 'postal_code')

# تسجيل النماذج في واجهة الإدارة
# admin.site.register(Users, UserAdmin)
admin.site.register(Address, AddressAdmin)


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users  # Adjust the import based on your app structure

class UserAdmin(BaseUserAdmin):
    model = Users
    list_display = ('name','username', 'email', 'phone', 'role', 'is_laundry_owner', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'phone', 'role', 'is_laundry_owner')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'role', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username', 'email', 'phone','name')
    ordering = ('username',)

# Register the custom user model with the customized admin
admin.site.register(Users, UserAdmin)
from django.contrib.auth.models import User, Group


# admin.site.unregister(User)
# admin.site.unregister(Group)