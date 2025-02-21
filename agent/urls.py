from django.urls import path
from .views import SalesAgentOrderDetailView, add_sales_agent,success
from .views import SalesAgentOrdersByUserId
from .views import SalesAgentOrderList
from .views import SalesAgentOrdersByDateRange,OrderAgentListView,OrderAgentAcceptedListView

urlpatterns = [
    path('add/', add_sales_agent, name='add_sales_agent'),
    path('success/', success, name='success'),
    path('sales-agent-order/<int:order_id>/', SalesAgentOrderDetailView.as_view(), name='sales-agent-order-detail'),

    # جلب كل الطلبات الخاصة بالمندوب
    path('sales-agent-orders/user/<int:user_id>/', SalesAgentOrdersByUserId.as_view(), name='sales-agent-orders-by-user'),

    # path('api/agent-orders/date-range/from/<str:start_date>/to/<str:end_date>/', SalesAgentOrdersByDateRange.as_view(), name='sales-agent-orders-by-date-range'),
    path('agent-orders/date-range/from/<str:start_date>/to/<str:end_date>/user/<int:user_id>/', 
     SalesAgentOrdersByDateRange.as_view(), name='sales-agent-orders-by-date-range'),
    #  جلب جميع احالات لطلب معين 
    path('order-status/<int:order_id>/', SalesAgentOrderList.as_view(), name='sales-agent-orders-by-order'),
    # جلب الطلبات للمندوب الجديدة فقط
    path('get-order-agent/', OrderAgentListView.as_view(), name='get-order-agent'),
    path('get-order-agent-accepted/<int:user_id>', OrderAgentAcceptedListView.as_view(), name='get-order-agent-accepted'),

]


