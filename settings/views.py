from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import SlideShowImage
from .serializers import SlideShowImageSerializer

class SlideShowImageViewSet(viewsets.ModelViewSet):
    queryset = SlideShowImage.objects.all()
    serializer_class = SlideShowImageSerializer


from .models import Setting
from .serializers import SettingSerializer

class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer