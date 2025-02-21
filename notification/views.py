# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import status

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    # فلترة الإشعارات حسب المستخدم
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)  # الحصول على معرّف المستخدم من الـ URL
        if user_id is not None:
            return Notification.objects.filter(user_id=user_id,is_read=False)  # فلترة الإشعارات حسب المستخدم
        return Notification.objects.all()  # إذا لم يكن هناك معرّف مستخدم، إرجاع جميع الإشعارات

    # إضافة عملية مخصصة لتحديث حالة الإشعار إلى "مقروء"
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        try:
            notification = self.get_object()  # الحصول على الإشعار بناءً على الـ pk
            notification.is_read = True  # تحديث حالة القراءة
            notification.save()  # حفظ التحديث في قاعدة البيانات
            return Response({"message": "تم تحديث حالة الإشعار إلى مقروء."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "الإشعار غير موجود."}, status=status.HTTP_404_NOT_FOUND)
