from django.utils import timezone
from django.contrib import admin
from accounts.models import Transaction
from users.models import Users, Wallet
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.translation import gettext_lazy as _
from bidi.algorithm import get_display  # استيراد مكتبة bidi
from import_export.admin import ExportMixin, ImportExportModelAdmin
dark_blue = CMYKColor(1, 0.5, 0, 0.5)

# تسجيل الخط العربي
pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Regular.ttf'))

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

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'Amiri'  # استخدام الخط العربي
    title = Paragraph(get_display("تقرير العمليات المالية"), title_style)  # معالجة النصوص العربية
    elements.append(title)

    data = [['المستخدم', 'التاريخ', 'نوع المعاملة', 'المبلغ', 'مدين', 'دائن', 'نسبة الملحق', 'الوصف']]
    
    total_amount = 0
    total_debit = 0
    total_credit = 0
    total_malaq_ratio = 0

    for transaction in queryset:
        data.append([
            get_display(transaction.user.username),
            transaction.date.strftime('%Y-%m-%d'),
            get_display(transaction.transaction_type),
            str(transaction.amount),
            str(transaction.debit),
            str(transaction.credit),
            str(transaction.malaq_ratio),
            get_display(transaction.description),
        ])
        total_amount += float(transaction.amount)
        total_debit += float(transaction.debit)
        total_credit += float(transaction.credit)
        total_malaq_ratio += float(transaction.malaq_ratio)

    data.append([
        'الإجمالي', '', '', f"{total_amount:.2f}", f"{total_debit:.2f}", f"{total_credit:.2f}", f"{total_malaq_ratio:.2f}", ''
    ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), dark_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Amiri'),  # استخدام الخط العربي
        ('FONTNAME', (0, 1), (-1, -1), 'Amiri'),  # استخدام الخط العربي لبقية الجدول
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    pdf.build(elements)
    return response

generate_pdf_report.short_description = "Print report as PDF table"

@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
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

class WalletAdmin(ImportExportModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    search_fields = ['owner_name', 'user__username']

admin.site.register(Wallet, WalletAdmin)