from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlideShowImageViewSet
from .views import SettingViewSet,CheckUpdateView
from .views import send_otp_api, verify_otp

router = DefaultRouter()
router.register(r'slide-show', SlideShowImageViewSet)
router.register(r'delivery-setting', SettingViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('settings/', SettingViewSet.as_view({'get': 'list'}), name='settings-list'),
    path('check-update/', CheckUpdateView.as_view(), name='check-update'),

    path('sdk/v1/sendOTP', send_otp_api),
    path('sdk/v1/verifyOTP', verify_otp),
]
