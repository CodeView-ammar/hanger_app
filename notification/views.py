from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Notification
from .serializers import NotificationSerializer
from users.models import Users


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]  # معطل للاختبار
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Notification.objects.filter(user_id=user_id).order_by('-created_at')
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
def mark_notification_read(request, notification_id):
    """تعيين الإشعار كمقروء"""
    try:
        notification = Notification.objects.get(
            id=notification_id
        )
        notification.is_read = True
        notification.save()
        return Response({'message': 'تم تعيين الإشعار كمقروء'})
    except Notification.DoesNotExist:
        return Response({'error': 'الإشعار غير موجود'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def mark_all_notifications_read(request, user_id):
    """تعيين جميع الإشعارات كمقروءة"""
    try:
        notifications = Notification.objects.filter(
            user_id=user_id,
            is_read=False
        )
        updated_count = notifications.update(is_read=True)
        return Response({'message': f'تم تعيين {updated_count} إشعار كمقروء'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def unread_notifications_count(request, user_id):
    """عدد الإشعارات غير المقروءة"""
    try:
        count = Notification.objects.filter(
            user_id=user_id,
            is_read=False
        ).count()
        return Response({'unread_count': count})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
@api_view(['POST'])
def create_notification(request):
    """إنشاء إشعار جديد"""
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        notification = serializer.save()

        # إرسال الإشعار عبر WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{notification.user_id}',  # استبدل user_id بالمعرف الصحيح
            {
                'type': 'send_notification',
                'notification': notification.message,  # يمكنك إرسال البيانات التي تحتاجها
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_notification(request, notification_id):
    """حذف إشعار"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.delete()
        return Response({'message': 'تم حذف الإشعار'}, status=status.HTTP_204_NO_CONTENT)
    except Notification.DoesNotExist:
        return Response({'error': 'الإشعار غير موجود'}, status=status.HTTP_404_NOT_FOUND)


def send_order_status_notification(user, order, new_status):
    """إرسال إشعار عند تغيير حالة الطلب"""
    status_messages = {
        'pending': 'تم استلام طلبك وهو في انتظار المعالجة',
        'confirmed': 'تم تأكيد طلبك بنجاح',
        'courier_assigned': 'تم تعيين مندوب لاستلام طلبك',
        'courier_on_the_way': 'المندوب في الطريق لاستلام طلبك',
        'delivered_to_laundry': 'تم تسليم طلبك للمغسلة',
        'in_progress': 'طلبك قيد المعالجة في المغسلة',
        'ready_for_delivery': 'طلبك جاهز للتسليم',
        'courier_accepted': 'تم قبول طلبك من المندوب',
        'delivered_to_customer': 'تم تسليم طلبك بنجاح',
        'completed': 'تم إكمال طلبك بنجاح',
        'canceled': 'تم إلغاء طلبك'
    }
    
    message = status_messages.get(new_status, f'تم تحديث حالة الطلب إلى {new_status}')
    
    notification = Notification.objects.create(
        user=user,
        message=f'الطلب رقم {order.id}: {message}',
        status='confirmation' if new_status in ['completed', 'delivered_to_customer'] else 'alert'
    )
    
    return notification


