from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone

from .models import SupportTicket, SupportMessage, SupportFAQ
from .serializers import (
    SupportTicketSerializer, SupportTicketCreateSerializer,
    SupportMessageSerializer, SupportMessageCreateSerializer,
    SupportFAQSerializer
)
from rest_framework import status
from users.models import Users  # تأكد أن لديك موديل المستخدم مرتبط برقم الهاتف




class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    # permission_classes = [IsAuthenticated]  # معطل للاختبار
    
    def get_queryset(self):
        # للاختبار نعيد جميع التذاكر
        return SupportTicket.objects.all().prefetch_related('messages')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SupportTicketCreateSerializer
        return SupportTicketSerializer
    
    def perform_create(self, serializer):
        # للاختبار نستخدم المستخدم رقم 5
        from users.models import Users
        user_id = self.request.data.get('user')

        if not user_id:
            raise serializers.ValidationError({"user": "معرف المستخدم مطلوب"})

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise serializers.ValidationError({"user": "المستخدم غير موجود"})

    
    @action(detail=True, methods=['post'])
    def assign_to_staff(self, request, pk=None):
        """تعيين التذكرة لموظف دعم فني"""
        ticket = self.get_object()
        staff_id = request.data.get('staff_id')
        
        if staff_id:
            try:
                from users.models import Users
                staff_member = Users.objects.get(id=staff_id, is_staff=True)
                ticket.assigned_to = staff_member
                ticket.status = 'in_progress'
                ticket.save()
                
                # إضافة رسالة نظام
                SupportMessage.objects.create(
                    ticket=ticket,
                    sender=staff_member,
                    message_type='system',
                    content=f'تم تعيين التذكرة للموظف: {staff_member.name}'
                )
                
                return Response({'message': 'تم تعيين التذكرة بنجاح'})
            except:
                return Response({'error': 'موظف غير صالح'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'معرف الموظف مطلوب'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def close_ticket(self, request, pk=None):
        """إغلاق التذكرة"""
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.resolved_at = timezone.now()
        ticket.save()
        
        # إضافة رسالة نظام
        SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message_type='system',
            content='تم إغلاق التذكرة'
        )
        
        return Response({'message': 'تم إغلاق التذكرة بنجاح'})


class SupportMessageViewSet(viewsets.ModelViewSet):
    serializer_class = SupportMessageSerializer
    # permission_classes = [IsAuthenticated]  # معطل للاختبار
    
    def get_queryset(self):
        ticket_id = self.request.query_params.get('ticket_id')
        if ticket_id:
            return SupportMessage.objects.filter(ticket_id=ticket_id)
        return SupportMessage.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SupportMessageCreateSerializer
        return SupportMessageSerializer
    
    def perform_create(self, serializer):
        # للاختبار نستخدم المستخدم رقم 5
        from users.models import Users
        user = Users.objects.get(id=5)
        serializer.save(sender=user)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """تعيين رسائل كمقروءة"""
        ticket_id = request.data.get('ticket_id')
        message_ids = request.data.get('message_ids', [])
        
        if ticket_id:
            queryset = SupportMessage.objects.filter(ticket_id=ticket_id)
            if message_ids:
                queryset = queryset.filter(id__in=message_ids)
            
            updated_count = queryset.update(is_read=True)
            return Response({'message': f'تم تعيين {updated_count} رسالة كمقروءة'})
        
        return Response({'error': 'معرف التذكرة مطلوب'}, status=status.HTTP_400_BAD_REQUEST)


class SupportFAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SupportFAQ.objects.filter(is_active=True)
    serializer_class = SupportFAQSerializer
    
    @action(detail=False)
    def by_category(self, request):
        """عرض الأسئلة الشائعة مجمعة حسب التصنيف"""
        categories = {}
        faqs = self.get_queryset()
        
        for faq in faqs:
            if faq.category not in categories:
                categories[faq.category] = []
            categories[faq.category].append(SupportFAQSerializer(faq).data)
        
        return Response(categories)


@api_view(['GET'])
def support_statistics(request):
    """إحصائيات الدعم الفني"""
    stats = {
        'total_tickets': SupportTicket.objects.count(),
        'open_tickets': SupportTicket.objects.filter(status='open').count(),
        'in_progress_tickets': SupportTicket.objects.filter(status='in_progress').count(),
        'resolved_tickets': SupportTicket.objects.filter(status='resolved').count(),
        'closed_tickets': SupportTicket.objects.filter(status='closed').count(),
    }
    
    # إحصائيات حسب التصنيف
    category_stats = SupportTicket.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    stats['by_category'] = list(category_stats)
    
    return Response(stats)


@api_view(['GET'])
def user_support_summary(request, user_id):
    """ملخص دعم فني للمستخدم"""
    user_tickets = SupportTicket.objects.filter(user_id=user_id)
    
    summary = {
        'total_tickets': user_tickets.count(),
        'open_tickets': user_tickets.filter(status='open').count(),
        'resolved_tickets': user_tickets.filter(status__in=['resolved', 'closed']).count(),
        'recent_tickets': SupportTicketSerializer(
            user_tickets[:5], many=True
        ).data
    }
    
    return Response(summary)





@api_view(['POST'])
def support_chat_api(request):
    """
    API يستقبل رسالة من المستخدم (عبر رقم الجوال) ويرد برسالة تلقائية
    """
    phone = request.data.get('phone')
    message = request.data.get('message')

    if not phone or not message:
        return Response({'error': 'الرجاء إدخال رقم الجوال والرسالة'}, status=status.HTTP_400_BAD_REQUEST)

    # محاولة جلب المستخدم بناءً على رقم الجوال
    try:
        user = Users.objects.get(phone=phone)
    except Users.DoesNotExist:
        return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)
    print("aaa"*10)
    print(user.id)
    # محاولة إيجاد تذكرة مفتوحة لهذا المستخدم
    ticket = SupportTicket.objects.filter(user=user, status__in=['open', 'in_progress']).first()

    # إذا لم توجد، أنشئ تذكرة جديدة
    if not ticket:
        ticket = SupportTicket.objects.create(
            user=user,
            title='رسالة من التطبيق',
            category='عام',
            status='open',
            created_at=timezone.now(),
        )

    # إنشاء الرسالة
    SupportMessage.objects.create(
        ticket=ticket,
        sender_id=user.id,
        message_type='user',
        content=message,
        is_read=False
    )

    # يمكنك وضع منطق الرد التلقائي هنا:
    auto_reply = "شكرًا لتواصلك معنا، سيتم الرد عليك قريبًا."

    # # إضافة رسالة النظام كرد تلقائي (اختياري)
    # SupportMessage.objects.create(
    #     ticket=ticket,
    #     sender=None,
    #     message_type='system',
    #     content=auto_reply,
    #     is_read=False
    # )

    return Response({
        'message': 'تم إرسال الرسالة بنجاح',
        'reply': auto_reply,
        'ticket_id': ticket.id
    })
@api_view(['GET'])
def get_support_messages(request):
    ticket_id = request.query_params.get('ticket_id')
    if not ticket_id:
        return Response({'error': 'يرجى إرسال ticket_id'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ticket = SupportTicket.objects.get(id=ticket_id)
    except SupportTicket.DoesNotExist:
        return Response({'error': 'التذكرة غير موجودة'}, status=status.HTTP_404_NOT_FOUND)

    messages = SupportMessage.objects.filter(ticket=ticket).order_by('created_at')
    serializer = SupportMessageSerializer(messages, many=True)
    return Response(serializer.data)