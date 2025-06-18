from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaundryOrdersByDateRange, LaundryViewSet,UserLaundryMarkViewSet ,user_laundry_mark_detail,user_laundry_mark_list,user_laundry_mark_delete

from services.views import LaundryServiceViewSet,ServiceCategoryViewSet,SubServiceViewSet
from .views import add_laundry
from .views import LaundryListByUser
from .views import OrderLaundryListView

router = DefaultRouter()
router.register(r'laundries', LaundryViewSet)
router.register(r'categores', ServiceCategoryViewSet)
router.register(r'user_laundry_marks', UserLaundryMarkViewSet)
router.register(r'laundry-services', LaundryServiceViewSet)
router.register(r'subservices', SubServiceViewSet, basename='subservice')

urlpatterns = [
    path('', include(router.urls)),
    # path('user_laundry_marks/', user_laundry_mark_list, name='user_laundry_mark_list'),
    path('user_laundry_marks_a/<int:pk>/', user_laundry_mark_detail, name='user_laundry_mark_detail'),
    path('user_laundry_marks_delete/<int:pk>/<int:laundry_id>/', user_laundry_mark_delete, name='user_laundry_marks_delete'),
    path('laundries/user/<int:user_id>/', LaundryListByUser.as_view(), name='laundries_by_user'),

    path('add_laundry/', add_laundry, name='add_laundry'),
# جلب طلبات مغسلة معينة
    path('laundries/<int:laundry_id>/orders/', OrderLaundryListView.as_view(), name='laundry-orders'),
    path('laundry-orders/date-range/from/<str:start_date>/to/<str:end_date>/user/<int:user_id>/', 
     LaundryOrdersByDateRange.as_view(), name='laundry-orders-by-date-range'),
]



