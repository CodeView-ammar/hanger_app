from django.utils import timezone
from django.contrib import admin
from accounts.models import Transaction  # تأكد من استيراد نموذج المستخدم
from users.models import  Users  # تأكد من استيراد نموذج المستخدم
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.colors import CMYKColor
from django.utils.translation import gettext_lazy as _

dark_blue = CMYKColor(1, 0.5, 0, 0.5)

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
    title = Paragraph("Financial Operations Report", styles['Title'])
    elements.append(title)

    data = [['User', 'Date', 'Transaction Type', 'Amount', 'Debit', 'Credit', 'Description']]
    
    total_amount = 0
    total_debit = 0
    total_credit = 0

    for transaction in queryset:
        data.append([
            transaction.user.username,
            transaction.date.strftime('%Y-%m-%d'),
            transaction.transaction_type,
            str(transaction.amount),
            str(transaction.debit),
            str(transaction.credit),
            transaction.description,
        ])
        total_amount += float(transaction.amount)
        total_debit += float(transaction.debit)
        total_credit += float(transaction.credit)

    data.append([
        'Total', '', '', f"{total_amount:.2f}", f"{total_debit:.2f}", f"{total_credit:.2f}", ''
    ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), dark_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
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
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'transaction_type', 'amount', 'debit', 'credit', 'description')
    list_filter = (
        DateRangeFilter,  # استخدام الفلتر المخصص
        'transaction_type',
        'user__role',
    )
    search_fields = ('user__username', 'description')  # البحث باستخدام اسم المستخدم
    date_hierarchy = 'date'
    ordering = ('-date',)

    # تفعيل البحث التلقائي في حقل المستخدم
    autocomplete_fields = ('user',)  # تأكد من أن "user" هو الحقل ForeignKey إلى نموذج المستخدم

    actions = [generate_pdf_report]