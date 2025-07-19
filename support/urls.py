from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tickets', views.SupportTicketViewSet, basename='support-tickets')
router.register(r'messages', views.SupportMessageViewSet, basename='support-messages')
router.register(r'faq', views.SupportFAQViewSet, basename='support-faq')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', views.support_statistics, name='support-statistics'),
    path('user/<int:user_id>/summary/', views.user_support_summary, name='user-support-summary'),
    path('support-chat/', views.support_chat_api, name='support_chat_api'),
    # مسار لجلب الرسائل (GET)
    path('support-chat/messages/', views.get_support_messages, name='support_chat_api_get_messages'),
]