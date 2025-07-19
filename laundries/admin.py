from django.contrib import admin

from services.models import LaundryService, Service
from .models import Laundry
from .models import Laundry, LaundryHours,UserLaundryMark
from import_export.admin import ExportMixin, ImportExportModelAdmin


# from .models import LaundryService

class LaundryHoursInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = LaundryHours
    extra = 1  # Number of empty forms to display

@admin.register(Laundry)
class LaundryAdmin(ImportExportModelAdmin):
    list_display = ('owner', 'name', 'address', 'phone', 'email', 'created_at', 'updated_at','owner_id','sales_percentage')
    inlines = [LaundryHoursInline]  # إضافة Inlines لنموذجي الخدمات وساعات العمل

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Laundry)
def after_laundry_save(sender, instance, created, **kwargs):
    if created:
        # عند إنشاء كائن Laundry جديد، نقوم بإنشاء LaundryService لجميع الخدمات
        services = Service.objects.all()
        for service in services:
            LaundryService.objects.create(
                laundry=instance,  # ربط الخدمة الجديدة بـ laundry
                service=service
            )
    else:
        LaundryService.objects.filter(laundry=instance).update(laundry=instance)


@admin.register(UserLaundryMark)
class UserLaundryMarkAdmin(ImportExportModelAdmin):
    list_display = ("user","laundry","added_at")
    