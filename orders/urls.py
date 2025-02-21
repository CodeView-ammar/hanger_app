# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderDetailsView, OrderItemView, OrderListView, OrderStatusView, PaymentMethodsDetailsViewSet,remove_item_from_cart,getPaymentMethodViewSet,PaymentMethodViewSet,CreateOrderView,OrderStatusUpdateView,OrderStatusUpdateLaundryView

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'add-payment-method', PaymentMethodViewSet, basename='payment-method')
router.register(r'payment-methods', getPaymentMethodViewSet, basename='payment-methods')
router.register(r'payment-methods-details', PaymentMethodsDetailsViewSet, basename='payment-methods-details')

from .views import OrderViewSet, OrderItemViewSet

router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'submit-order', CreateOrderView,basename='submit-order')
router.register(r'orders-user', OrderListView,basename='view-order')
router.register(r'orders-laundry', OrderDetailsView,basename='view-laundry-order')
router.register(r'orders-items', OrderItemView, basename='orders-items')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/filter/', CartViewSet.as_view({'get': 'filter_by_user_and_laundry'}), name='cart-filter'),
    path('cart/update/', CartViewSet.as_view({'get': 'user_by_user_and_laundry'}), name='cart-update'),
    path('orders-status/', OrderStatusView.as_view({'get': 'last_order_status'}), name='orders-status'),
    
    path('cart/delete/', remove_item_from_cart, name='cart-delete'),
    # path('order/<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('order/<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    # تحديث حالة الطلب عن طريق المغسلة
    path('order/<int:pk>/update-laundryorder/', OrderStatusUpdateLaundryView.as_view(), name='order-status-Laundry-update'),

]
