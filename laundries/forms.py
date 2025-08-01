from django import forms
from .models import Laundry
from users.models import Users
from django.core.exceptions import ValidationError


class LaundryForm(forms.ModelForm):
    class Meta:
        model = Laundry
        fields = [
            'owner_name', 
            'name', 
            'address', 
            'phone', 
            'email', 
            'image', 
            'license_image', 
            'commercial_record_image', 
            'x_map',  # Add these fields
            'y_map',
        ]
        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if Users.objects.filter(phone=phone).exists():
                raise ValidationError("رقم الهاتف موجود بالفعل.")
            return phone
        def clean_email(self):
            print('@'*90)
            email = self.cleaned_data.get('email')
            if Laundry.objects.filter(email=email).exists():
                raise ValidationError("البريد الإلكتروني موجود بالفعل.")
        # def clean_name(self):
        #     phone = self.cleaned_data.get('phone')
        #     if Users.objects.filter(username=phone).exists():
        #         raise ValidationError("رقم الهاتف موجود بالفعل.")
        #     return phone
            
