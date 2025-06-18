from django.urls import path
from .views import TransactionCreateAPIView,WalletView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionCreateAPIView, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('wallet/', WalletView.as_view(), name='user-wallet'),
]

