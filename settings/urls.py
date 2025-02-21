from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlideShowImageViewSet
from .views import SettingViewSet

router = DefaultRouter()
router.register(r'slide-show', SlideShowImageViewSet)
router.register(r'delivery-setting', SettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', SettingViewSet.as_view({'get': 'list'}), name='settings-list'),
]
