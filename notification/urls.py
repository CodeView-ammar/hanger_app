from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.NotificationListView.as_view(), name='user-notifications'),
    path('user/<int:user_id>/unread-count/', views.unread_notifications_count, name='unread-count'),
    path('user/<int:user_id>/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('<int:notification_id>/mark_as_read/', views.mark_notification_read, name='mark-read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete-notification'),
    path('create/', views.create_notification, name='create-notification'),

    path('send-test-notification/', views.SendTestNotificationView.as_view(), name='send-test-notification'),
]