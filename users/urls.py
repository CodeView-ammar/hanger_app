from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,user_phone,AddressViewSet,user_phone_login,AddressDetailView
# from .views import UserViewSet, user_management,create_auth
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)


from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('', include(router.urls)),
    path('address/<int:user_id>/', AddressDetailView.as_view(), name='address_detail'),
    path('user_phone/<str:phone>', user_phone, name='user_phone'),
    path('user_phone_login/<str:phone>', user_phone_login, name='user_phone_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('users/register/', create_auth),
    
  
]

