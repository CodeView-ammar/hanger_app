from django.contrib import admin
from .models import Laundry
from .models import Laundry, LaundryHours,UserLaundryMark


# from .models import LaundryService

class LaundryHoursInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = LaundryHours
    extra = 1  # Number of empty forms to display

# class LaundryServiceInline(admin.TabularInline):  # يمكنك استخدام StackedInline إذا كنت تفضل ذلك
#     model = LaundryService
#     extra = 1  # عدد الصفوف الفارغة لإضافة خدمات جديدة
#     fields = ('service', 'name', 'price', 'urgent_price', 'duration')  # الحقول التي ترغب في عرضها
#     # يمكنك إضافة أي خيارات أخرى حسب الحاجة
@admin.register(Laundry)
class LaundryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'address', 'phone', 'email', 'created_at', 'updated_at','owner_id')
    inlines = [LaundryHoursInline]  # إضافة Inlines لنموذجي الخدمات وساعات العمل


@admin.register(UserLaundryMark)
class UserLaundryMarkAdmin(admin.ModelAdmin):
    list_display = ("user","laundry","added_at")
    