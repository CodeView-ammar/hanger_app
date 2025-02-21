from django import forms
from django.core.exceptions import ValidationError
from .models import SalesAgent

def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 1 MB limit
    if value.size > max_size:
        raise ValidationError(f"حجم الملف يجب أن لا يتجاوز {max_size / (1024 * 1024)} ميجابايت.")
class SalesAgentForm(forms.ModelForm):

    CITY_CHOICES = [
        ('riyadh', 'الرياض'),
        ('dammam', 'الدمام'),
        ('jeddah', 'جدة'),
        ('khobar', 'الخبر'),
        ('mecca', 'مكة المكرمة'),
        ('medina', 'المدينة المنورة'),
    ]
    
    VEHICLE_TYPE_CHOICES = [
        ('car', 'سيارة'),
        ('motorcycle', 'دراجة نارية'),
        ('bicycle', 'دراجة هوائية'),
    ]

    city = forms.ChoiceField(choices=CITY_CHOICES, label="المدينة")
    vehicle_type = forms.ChoiceField(choices=VEHICLE_TYPE_CHOICES, label="نوع المركبة")
    class Meta:
        model = SalesAgent
        fields = ['name', 'phone', 'email', 'region', 'id_number', 'id_image', 'license_number', 'license_image', 'city','vehicle_type']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'id_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        print('@'*90)
        email = self.cleaned_data.get('email')
        if SalesAgent.objects.filter(email=email).exists():
            raise ValidationError("البريد الإلكتروني موجود بالفعل.")
        return email
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if SalesAgent.objects.filter(id_number=id_number).exists():
            raise ValidationError("رقم الهوية موجود بالفعل.")
        return id_number
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if SalesAgent.objects.filter(phone=phone).exists():
            raise ValidationError("رقم الهاتف موجود بالفعل.")
        return phone


    def clean_id_image(self):
        id_image = self.cleaned_data.get('id_image')
        if id_image:
            validate_file_size(id_image)  # تحقق من حجم الصورة
        return id_image

    def clean_license_image(self):
        license_image = self.cleaned_data.get('license_image')
        if license_image:
            validate_file_size(license_image)  # تحقق من حجم الصورة
        return license_image


