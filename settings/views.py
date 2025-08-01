from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import SlideShowImage,AppVersion
from .serializers import SlideShowImageSerializer,AppVersionSerializer

class SlideShowImageViewSet(viewsets.ModelViewSet):
    queryset = SlideShowImage.objects.all()
    serializer_class = SlideShowImageSerializer


from .models import Setting
from .serializers import SettingSerializer

class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AppVersion

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