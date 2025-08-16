from django.utils import timezone
from django.contrib import admin
from accounts.models import Transaction,Statistics
from users.models import Wallet,Users
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.translation import gettext_lazy as _
from reportlab.lib.units import cm
# مكتبات دعم العربية
import arabic_reshaper
from bidi.algorithm import get_display
from django.urls import reverse
from django.utils.html import format_html
# مكتبة التصدير والاستيراد
from import_export.admin import ImportExportModelAdmin
from decimal import Decimal
            
# تسجيل الخط العربي
pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Regular.ttf'))

# اللون الرئيسي للترويسة
dark_blue = CMYKColor(1, 0.5, 0, 0.5)

def reshape_arabic_text(text):
    """يعيد تشكيل النص العربي لعرضه بشكل صحيح في PDF"""
    if not text:
        return ""
    try:
        reshaped_text = arabic_reshaper.reshape(str(text))
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return str(text)

class DateRangeFilter(admin.SimpleListFilter):
    title = _('Date Range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('this_week', _('This Week')),
            ('this_month', _('This Month')),
            ('this_year', _('This Year')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(date=timezone.now().date())
        if self.value() == 'this_week':
            return queryset.filter(date__week=timezone.now().date().isocalendar()[1])
        if self.value() == 'this_month':
            return queryset.filter(date__month=timezone.now().date().month)
        if self.value() == 'this_year':
            return queryset.filter(date__year=timezone.now().date().year)

def generate_pdf_report(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=60)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'Amiri'
    title_style.fontSize = 22
    title_style.alignment = 1  # Center

    # عنوان التقرير
    title = Paragraph(reshape_arabic_text("تقرير العمليات المالية"), title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.4 * cm))

    # رأس الجدول
    data = [[
        reshape_arabic_text('المستخدم'),
        reshape_arabic_text('التاريخ'),
        reshape_arabic_text('نوع المعاملة'),
        reshape_arabic_text('المبلغ'),
        reshape_arabic_text('مدين'),
        reshape_arabic_text('دائن'),
        reshape_arabic_text('نسبة الملحق'),
        reshape_arabic_text('الوصف'),
    ]]

    total_amount = total_debit = total_credit = total_malaq_ratio = 0

    for transaction in queryset:
        row = [
            reshape_arabic_text(transaction.user.username),
            transaction.date.strftime('%Y-%m-%d'),
            reshape_arabic_text(transaction.transaction_type),
            f"{transaction.amount:.2f}",
            f"{transaction.debit:.2f}",
            f"{transaction.credit:.2f}",
            f"{transaction.malaq_ratio:.2f}",
            reshape_arabic_text(transaction.description),
        ]
        data.append(row)

        total_amount += float(transaction.amount)
        total_debit += float(transaction.debit)
        total_credit += float(transaction.credit)
        total_malaq_ratio += float(transaction.malaq_ratio)

    # صف الإجمالي
    data.append([
        reshape_arabic_text('الإجمالي'),
        '', '', f"{total_amount:.2f}",
        f"{total_debit:.2f}",
        f"{total_credit:.2f}",
        f"{total_malaq_ratio:.2f}",
        ''
    ])

    table = Table(data, colWidths=[3*cm, 2.8*cm, 3*cm, 2.2*cm, 2*cm, 2*cm, 2.2*cm, 4*cm], repeatRows=1)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Amiri'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), dark_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    # تظليل الصفوف بالتناوب
    for i in range(1, len(data) - 1):
        bg_color = colors.whitesmoke if i % 2 == 0 else colors.white
        table.setStyle([('BACKGROUND', (0, i), (-1, i), bg_color)])

    elements.append(table)

    # تذييل
    footer_style = styles['Normal']
    footer_style.fontName = 'Amiri'
    footer_style.fontSize = 10
    footer = Paragraph(reshape_arabic_text("تم إنشاء التقرير بتاريخ: ") + timezone.now().strftime('%Y-%m-%d %H:%M'), footer_style)
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(footer)

    pdf.build(elements)
    return response

generate_pdf_report.short_description = "Print report as PDF table"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'transaction_type', 'amount', 'debit', 'credit', 'malaq_ratio', 'description')
    list_filter = (
        DateRangeFilter,
        'transaction_type',
        'user__role',
    )
    search_fields = ('user__username', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
    autocomplete_fields = ('user',)
    actions = [generate_pdf_report]
    def has_add_permission(self, request):
        return False  # منع الإضافة

    def has_change_permission(self, request, obj=None):
        return False  # منع التعديل

    def has_delete_permission(self, request, obj=None):
        return False  # منع الحذف

    def get_import_formats(self):
        return []  # منع استيراد البيانات

    def get_export_formats(self):
        return []  # منع تصدير البيانات

from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wallet, Transaction
from import_export.admin import ImportExportModelAdmin

class WalletAdmin(ImportExportModelAdmin):
    list_display = ('owner_name', 'user', 'balance', 'created_at', 'updated_at', 'transfer_button')

    list_filter = ('status', 'created_at')
    
    search_fields = ['owner_name', 'user__username']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'laundry_owner':
            return qs.filter(user=request.user)
        return qs
    def transfer_button(self, obj):
        # تحقق مما إذا كان المستخدم هو صاحب المغسلة
        if obj.user.is_laundry_owner:  # تأكد من أن لديك هذا الحقل في نموذج المستخدم
            url = reverse('admin:transfer_funds', args=[obj.id])
            return format_html('<a class="button" href="{}">تحويل</a>', url)
        return ""  # لا تعرض أي شيء إذا لم يكن هو صاحب المغسلة

    transfer_button.short_description = 'تحويل'

    def transfer_funds(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)

        if request.method == 'POST':
            transfer_amount = Decimal(request.POST.get('amount', 0))

            if wallet.balance >= transfer_amount:
                wallet.balance -= transfer_amount
                wallet.save()

                Transaction.objects.create(
                    user=wallet.user,
                    transaction_type='transfer',
                    amount=Decimal(transfer_amount),
                    debit=0,
                    credit=transfer_amount,
                    description=f"تحويل مبلغ {transfer_amount} من طلب التحويل."
                )

                self.message_user(request, "تم التحويل بنجاح.")
                return redirect('..')  # العودة إلى قائمة المحفظات
            else:
                self.message_user(request, "الرصيد غير كافٍ لإجراء التحويل.", level='error')

        return render(request, 'admin/transfer_funds.html', {'wallet': wallet})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('transfer/<int:wallet_id>/', self.admin_site.admin_view(self.transfer_funds), name='transfer_funds'),
        ]
        return custom_urls + urls

admin.site.register(Wallet, WalletAdmin)


class StatsAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"  # يمكنك استخدام قالب مخصص هنا

    def changelist_view(self, request, extra_context=None):
        # إعداد الإحصائيات (يمكنك استبدال القيم بالاستعلامات الفعلية)
        laundries_count = 10  # استبدل هذا بالعدد الفعلي
        agents_count = 5      # استبدل هذا بالعدد الفعلي
        
        context = {
            'laundries_count': laundries_count,
            'agents_count': agents_count,
        }
        
        return super().changelist_view(request, extra_context=context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_site.admin_view(self.stats_view), name='stats'),
        ]
        return custom_urls + urls

    def stats_view(self, request):
        # عرض الإحصائيات
        laundries_count = 10  # استبدل هذا بالعدد الفعلي
        agents_count = 5      # استبدل هذا بالعدد الفعلي
        return HttpResponse(
            _("إحصائيات: عدد المغاسل: {}, عدد المناديب: {}").format(laundries_count, agents_count)
        )
