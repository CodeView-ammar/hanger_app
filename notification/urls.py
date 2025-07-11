from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# إنشاء الراوتر وتسجيل ViewSet
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),  # تضمين جميع URLs من الراوتر
]