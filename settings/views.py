from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AppVersion
from rest_framework import viewsets
from .models import SlideShowImage,AppVersion
from .serializers import SlideShowImageSerializer
from .models import Setting
from .serializers import SettingSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
import requests
from .models import OTPAPI
import requests

class SlideShowImageViewSet(viewsets.ModelViewSet):
    queryset = SlideShowImage.objects.all()
    serializer_class = SlideShowImageSerializer



class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer



class CheckUpdateView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        # الحصول على المعلمات من الاستعلام (query parameters)
        platform = request.query_params.get('platform')
        current_version = request.query_params.get('current_version')

        if platform not in ['android', 'ios']:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)

        if not current_version or not isinstance(current_version, str):
            return Response({'error': 'Current version is required and must be a string'}, status=status.HTTP_400_BAD_REQUEST)

        # البحث عن أحدث إصدار
        latest = AppVersion.objects.filter(platform=platform).order_by('-id').first()

        if not latest:
            return Response({'update': False})

        # مقارنة الإصدارات
        update_needed = version_compare(current_version, latest.version)

        return Response({
            'update': update_needed,  # true إذا كان الإصدار الحالي مساوياً أو أكبر
            'force_update': latest.force_update,
            'latest_version': latest.version,
            'message': latest.message,
        })

def version_compare(current_version, latest_version):
    # دالة للمقارنة بين الإصدارات
    current_tuple = tuple(map(int, current_version.split(".")))
    latest_tuple = tuple(map(int, latest_version.split(".")))

    # إرجاع True إذا كان الإصدار الحالي أكبر أو مساوٍ للإصدار الأخير
    return current_tuple >= latest_tuple

import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# الآن يمكنك الحصول على المتغير
API_SECRET = os.environ.get("api_token")

API_URL_SEND_OTP = "https://api.authentica.sa/api/sdk/v1/sendOTP"
API_URL_verify_OTP = "https://api.authentica.sa/api/sdk/v1/verifyOTP"


@api_view(['POST'])
def send_otp_api(request):
    phone = request.data.get("phone")
    if not phone:
        return Response({"status": False, "message": "رقم الجوال مطلوب"}, status=400)

    # إرسال عبر Authentica
    status_code, resp_data = send_sms_via_authentica(phone)

    if status_code == 200:
        return Response({"status": True, "message": "تم إرسال رمز التحقق",  "provider_response": resp_data})
    else:
        return Response({"status": False, "message": "فشل الإرسال", "error": resp_data}, status=500)

@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get("phone")
    otp = request.data.get("otp")

    # التحقق من وجود الحقول المطلوبة
    if not phone or not otp:
        return Response({"status": False, "message": "جميع الحقول مطلوبة"}, status=400)

    headers = {
        'Accept': 'application/json',
        'X-Authorization': API_SECRET,
        'Content-Type': 'application/json',
    }

    payload = {
        'phone': phone,
        'otp': otp,
        'method': 'sms',
    }

    # إرسال طلب التحقق
    response = requests.post(API_URL_verify_OTP, headers=headers, json=payload)

    if response.status_code == 200:
        # تحقق من وجود الرمز في قاعدة البيانات
        # otp_obj = OTPAPI.objects.filter(phone_number=phone, otp_code=otp, is_verified=False).latest('created_at')

        # if otp_obj.is_expired():
        #     return Response({"status": False, "message": "انتهت صلاحية الرمز"}, status=400)

        # # تحديث حالة التحقق
        # otp_obj.is_verified = True
        # otp_obj.save()

        return Response({"status": True, "message": "تم التحقق بنجاح"})
    else:
        return Response({
            "status": False,
            "message": f"فشل التحقق: {response.json().get('message', response.text)}"
        }, status=response.status_code)

    
    # except Exception as e:
    #     return Response({"status": False, "message": str(e)}, status=500)



def send_sms_via_authentica(phone):
    """إرسال OTP عبر API Authentica"""
    headers = {
        "Accept": "application/json",
        "X-Authorization": API_SECRET,
        "Content-Type": "application/json",
    }
    payload = {
        "phone": phone,
        "method": "sms",
        "number_of_digits": 4,
        "otp_format": "numeric",
        "is_fallback_on": 0,
    }
    try:
        response = requests.post(API_URL_SEND_OTP, headers=headers, json=payload)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}
