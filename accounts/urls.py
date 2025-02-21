from django.urls import path
from .views import TransactionCreateAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionCreateAPIView, basename='transactions')
urlpatterns = [
    path('', include(router.urls)),
]
