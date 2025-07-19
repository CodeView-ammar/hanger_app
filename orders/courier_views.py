from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, SalesAgentOrder
from .serializers import OrderSerializer
from agent.models import SalesAgent
from notification.models import Notification


class CourierOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoints للمندوبين لإدارة طلبات التوصيل
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def available_orders(self, request):
        """
        جلب الطلبات المتاحة للتوصيل
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'معرف المستخدم مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق من أن المستخدم مندوب
        try:
            agent = SalesAgent.objects.get(user_id=user_id)
        except SalesAgent.DoesNotExist:
            return Response({'error': 'المستخدم ليس مندوباً'}, status=status.HTTP_403_FORBIDDEN)

        # جلب الطلبات التي تحتاج توصيل ولم يتم قبولها بعد
        available_orders = Order.objects.filter(
            delivery_method='delivery',
            status='pending'
        ).exclude(
            sales_agent__isnull=False
        ).order_by('-order_date')

        serializer = self.get_serializer(available_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept_order(self, request, pk=None):
        """
        قبول طلب توصيل من قبل المندوب
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'معرف المستخدم مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = SalesAgent.objects.get(user_id=user_id)
            order = self.get_object()
        except SalesAgent.DoesNotExist:
            return Response({'error': 'المستخدم ليس مندوباً'}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({'error': 'الطلب غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        # التحقق من أن الطلب متاح للقبول
        if order.sales_agent is not None:
            return Response({'error': 'تم قبول هذا الطلب بالفعل'}, status=status.HTTP_400_BAD_REQUEST)

        if order.delivery_method != 'delivery':
            return Response({'error': 'هذا الطلب لا يحتاج توصيل'}, status=status.HTTP_400_BAD_REQUEST)

        # قبول الطلب
        order.sales_agent = agent
        order.status = 'courier_accepted'
        order.save()

        # إنشاء سجل في جدول SalesAgentOrder
        SalesAgentOrder.objects.create(
            sales_agent=agent,
            order=order,
            status='accepted',
            delivery_profit=10.0  # يمكن حسابها بناء على المسافة أو نسبة من المبلغ
        )

        # إنشاء إشعار للعميل
        Notification.objects.create(
            user=order.user,
            message=f'تم قبول طلبك رقم #{order.id} من قبل المندوب وسيتم التوصيل قريباً',
            status='confirmation'
        )

        return Response({
            'success': 'تم قبول الطلب بنجاح',
            'order_id': order.id,
            'status': order.status
        })

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        جلب طلبات المندوب
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'معرف المستخدم مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = SalesAgent.objects.get(user_id=user_id)
        except SalesAgent.DoesNotExist:
            return Response({'error': 'المستخدم ليس مندوباً'}, status=status.HTTP_403_FORBIDDEN)

        # جلب طلبات المندوب
        my_orders = Order.objects.filter(sales_agent=agent).order_by('-order_date')
        serializer = self.get_serializer(my_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        تحديث حالة الطلب من قبل المندوب
        """
        user_id = request.data.get('user_id')
        new_status = request.data.get('status')
        
        if not user_id or not new_status:
            return Response({'error': 'معرف المستخدم وحالة الطلب مطلوبان'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = SalesAgent.objects.get(user_id=user_id)
            order = self.get_object()
        except SalesAgent.DoesNotExist:
            return Response({'error': 'المستخدم ليس مندوباً'}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({'error': 'الطلب غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        # التحقق من أن الطلب مخصص لهذا المندوب
        if order.sales_agent != agent:
            return Response({'error': 'ليس لديك صلاحية لتعديل هذا الطلب'}, status=status.HTTP_403_FORBIDDEN)

        # تحديث حالة الطلب
        order.status = new_status
        order.save()

        # إنشاء إشعار للعميل بناء على الحالة الجديدة
        status_messages = {
            'courier_on_the_way': 'المندوب في الطريق إليك',
            'picked_up_from_customer': 'تم استلام الطلب منك',
            'delivered_to_laundry': 'تم تسليم الطلب للمغسلة',
            'delivery_by_courier': 'المندوب في طريقه لتوصيل الطلب',
            'delivered_to_customer': 'تم تسليم الطلب'
        }

        if new_status in status_messages:
            Notification.objects.create(
                user=order.user,
                message=f'طلبك رقم #{order.id}: {status_messages[new_status]}',
                status='alert'
            )

        return Response({
            'success': 'تم تحديث حالة الطلب',
            'order_id': order.id,
            'status': order.status
        })