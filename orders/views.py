from accounts.models import Transaction
from notification.fcm_service import FCMService
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.decorators import action
from users.models import Users
from .models import Cart, LaundryOrder, PaymentDetail,PaymentMethod, PaymentMethodsDetails, SalesAgentOrder, Service,Order,OrderItem
from .serializers import CartSerializer, OrderCustomSerializer, OrderItemSerializer_c, OrderStatusUpdateLaundrySerializer,PaymentMethodSerializer,PaymentMethodsDetailsSerializer, ServiceSerializer
from .serializers import OrderSerializer, OrderItemSerializer
from .serializers import OrderStatusUpdateSerializer
from agent.models import SalesAgent
from laundries.models import Laundry
from settings.models import Setting
from decimal import Decimal
    


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request):
        user_id = request.data.get('user')
        laundry_id = request.data.get('laundry')
        service_id = request.data.get('service')
        price = request.data.get('price')
        quantity = request.data.get('quantity')
        service_type= request.data.get("service_type")
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error': 'الكمية يجب أن تكون عدد صحيح'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user_id=user_id, laundry_id=laundry_id, service_id=service_id)
            cart.quantity += quantity
            cart.price = price
            cart.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            cart_data = {
                'user': user_id,
                'laundry': laundry_id,
                'service': service_id,
                'price': price,
                'quantity': quantity,
                "service_type":service_type,
            }
            cart_serializer = CartSerializer(data=cart_data)
            if cart_serializer.is_valid():
                cart = cart_serializer.save()
                return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
            return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter_by_user_and_laundry(self, request):
        user_id = request.query_params.get('user')
        laundry_id = request.query_params.get('laundry')

        if not user_id or not laundry_id:
            return Response({'error': 'مطلوب اسم المستخدم ومعرف المغسلة'}, status=status.HTTP_400_BAD_REQUEST)

        carts = Cart.objects.filter(user_id=user_id, laundry_id=laundry_id)
        total_price = sum(cart.price * cart.quantity for cart in carts)

        services = Service.objects.filter(laundry_id=laundry_id)
        services_data = ServiceSerializer(services, many=True).data

        cart_data = CartSerializer(carts, many=True).data
        response_data = {
            'carts': cart_data,
            'total_price': total_price,
            'services': services_data,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

    def user_by_user_and_laundry(self, request):
        user_id = request.query_params.get('user')
        laundry_id = request.query_params.get('laundry')
        service_id = request.query_params.get('service')
        quantity = request.query_params.get('quantity')
        
        if not user_id or not laundry_id or not service_id or not quantity:
            return Response({'error': 'مطلوب اسم المستخدم ومعرف المغسلة'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the quantity
        updated_rows = Cart.objects.filter(user_id=user_id, laundry_id=laundry_id, service_id=service_id).update(quantity=int(quantity))

        if updated_rows > 0:
            # Retrieve the updated cart items
            updated_carts = Cart.objects.filter(user_id=user_id, laundry_id=laundry_id, service_id=service_id)
            cart_data = CartSerializer(updated_carts, many=True).data
            response_data = {
                'carts': cart_data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'لم يتم العثور على السلة لتحديثها'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def remove_item_from_cart(request):
    # Extract user, laundry, and service identifiers
    user_id = request.query_params.get('user')
    laundry_id = request.query_params.get('laundry')
    service_id = request.query_params.get('service')

    if not user_id or not laundry_id or not service_id:
        return Response({'error': 'User, Laundry, and Service are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_item = Cart.objects.get(user_id=user_id, laundry_id=laundry_id, service_id=service_id)
        cart_item.delete()  # Remove the item from the cart
        return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


class getPaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def list(self, request, *args, **kwargs):
        """ جلب طريقة الدفع الافتراضية بناءً على معرف المستخدم """
        
        user_id = request.query_params.get('user')  # استلام `user` من الـ URL
        print(f"🔹 تم استقبال user_id: {user_id}")  # طباعة معرف المستخدم لفحصه

        if not user_id:
            return Response({'detail': 'يرجى تحديد معرف المستخدم (user) في الرابط'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_payment_method = PaymentMethod.objects.filter(user_id=user_id, default=True, is_active=True).first()
            print(f"🔹 نتيجة البحث عن طريقة الدفع: {existing_payment_method}")  # طباعة النتيجة لفحصها

            if existing_payment_method:
                serializer = self.get_serializer(existing_payment_method)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({'detail': 'لم يتم العثور على طريقة دفع افتراضية'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"❌ خطأ في جلب بيانات الدفع: {e}")  # طباعة أي خطأ يحدث
            return Response({'error': 'حدث خطأ غير متوقع في السيرفر'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def create(self, request, *args, **kwargs):
        payment_method_name = request.data.get('name')
        payment_method_user = request.data.get('user')
        
        # تحقق مما إذا كانت طريقة الدفع موجودة بالفعل
        existing_payment_method = PaymentMethod.objects.filter(name=payment_method_name,user_id=payment_method_user).first()

        if existing_payment_method:
            # إذا كانت موجودة، ضبط جميع طرق الدفع كغير افتراضية
            # PaymentMethod.objects.all().update(default=False)
            # ضبط القيمة المختارة كافتراضية
            existing_payment_method.default = True
            existing_payment_method.save()
            serializer = self.get_serializer(existing_payment_method)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # إذا لم تكن موجودة، ضبط جميع طرق الدفع كغير افتراضية
            # PaymentMethod.objects.all().update(default=False)

            # إضافة القيمة الجديدة
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentMethodsDetailsViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethodsDetails.objects.all()
    serializer_class = PaymentMethodsDetailsSerializer

    def create(self, request, *args, **kwargs):
        payment_method_name = request.data.get('payment_method')
        try:
            payment_method = PaymentMethod.objects.get(name=payment_method_name)
        except PaymentMethod.DoesNotExist:
            return Response({'error': 'Payment method does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # إعداد البيانات الجديدة مع ربط payment_method
        request.data['payment_method'] = payment_method.id  # احصل على ID بعد العثور عليه
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        payment_method_name = request.data.get('payment_method')
        if payment_method_name:
            try:
                payment_method = PaymentMethod.objects.get(name=payment_method_name)
                request.data['payment_method'] = payment_method.id
            except PaymentMethod.DoesNotExist:
                return Response({'error': 'Payment method does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

from django.db import IntegrityError
from django.http import JsonResponse

class CreateOrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        user_id = request.data.get('userId')
        laundry_id = request.data.get('laundryId')
        delegate_note = request.data.get('delegateNote')
        payment_method = request.data.get('paymentMethod')
        isPaid = request.data.get('isPaid')
        totalAmount = request.data.get('totalAmount')
        

        if not user_id: 
            return Response({'detail': 'userId'}, status=status.HTTP_400_BAD_REQUEST)
        if not laundry_id:
        
            return Response({'detail': 'laundry_id'}, status=status.HTTP_400_BAD_REQUEST)
        if not payment_method:
            return Response({'detail': 'paymentMethod'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch cart items
        cart_items = Cart.objects.filter(user_id=user_id, laundry_id=laundry_id)
        
        if not cart_items.exists():
            return Response({'detail': 'There are no items in the shopping cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total amount
        # total_amount = sum(item.price * item.quantity for item in cart_items)
        total_amount =totalAmount
        
        try:
            payment_method_instance = PaymentMethod.objects.get(name=payment_method, user_id=user_id)
        except PaymentMethod.DoesNotExist:
            return Response({'detail': 'Payment method not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Create the order
            order = Order.objects.create(
                user_id=user_id,
                laundry_id=laundry_id,
                total_amount=total_amount,
                status='pending',
                payment_status='paid' if isPaid else 'unpaid',
                payment_method=payment_method_instance
            )
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                service_id=cart_item.service_id,
                service_type=cart_item.service_type,
                quantity=cart_item.quantity,
                price=cart_item.price,
                notes=delegate_note
            )

        # Create payment detail
        PaymentDetail.objects.create(
            order=order,
            amount=total_amount,
            payment_method=payment_method_instance,
            transaction_id=f'TXN-{order.id}',  # مثال على كيفية إنشاء معرف المعاملة
            status='successful' if isPaid else 'pending',
            note=f'طلب جديد رقم: TXN-{order.id}'
        )
        # if(isPaid):
        Transaction.objects.create(
            user_id=user_id,
            transaction_type="withdraw",
            amount=total_amount,
            debit=0,
            credit=total_amount,
            description=f"خصم مقابل فاتورة #{order.id}"
        )
    
        # Delete cart items
        cart_items.delete()
        PaymentMethod.objects.all().update(default=False)
        
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"}, status=404)

        if not user.fcm:
            return JsonResponse({"success": False, "error": "FCM token غير موجود للمستخدم"}, status=400)

        # إرسال الإشعار
        FCMService.send_message(token=user.fcm, title="طلب جديد", body="تم إنشاء الطلب")


        # Return the created order response
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView

class CustomerReceiveOrderView(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'الطلب غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        # if order.status != 'courier_accepted_end':
        #     return Response({'error': f'لا يمكن تغيير الحالة من {order.status} إلى customer_received'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'delivered_to_customer'
        order.save()

        # إذا أردت تسجيل عملية مالية عند استلام العميل، يمكنك تفعيل هذا الجزء:
        # Transaction.objects.create(
        #     user_id=order.user_id,
        #     transaction_type='deposit',
        #     amount=order.total_amount,
        #     debit=order.total_amount,
        #     credit=0,
        #     description='استلام العميل للطلب'
        # )

        return Response({'success': 'تم تحديث حالة الطلب إلى استلام العميل'}, status=status.HTTP_200_OK)
class CanceledReceiveOrderView(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'الطلب غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        order.status = 'canceled'
        order.save()


        return Response({'success': 'تم تحديث حالة الطلب إلى استلام العميل'}, status=status.HTTP_200_OK)

class OrderListView(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # تحديد الاستعلام الافتراضي
    serializer_class = OrderCustomSerializer  # تحديد الـ Serializer

    def get_queryset(self):
        # التصفية بناءً على `user_id` من الـ query params
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            # إذا تم تقديم user_id، قم بتصفية النتائج ثم ترتيبها حسب الأحدث
            return Order.objects.filter(user_id=user_id).order_by('-order_date')  # ترتيب الأحدث أولاً
        return Order.objects.all().order_by('-order_date')  # ترتيب الأحدث أولاً


class OrderStatusView(viewsets.ModelViewSet):

    queryset = Order.objects.all()  # تحديد الاستعلام الافتراضي
    serializer_class = OrderCustomSerializer  # تحديد الـ Serializer

    def get_queryset(self):
        """
        تقوم هذه الدالة بتصفية الطلبات بناءً على `user_id` من المعاملات الخاصة بالـ query.
        وترجع الطلبات مرتبة حسب الأحدث أولاً.
        """
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            return Order.objects.filter(user_id=user_id).order_by('-order_date')  # ترتيب الأحدث أولاً
        return Order.objects.all().order_by('-order_date')  # ترتيب الأحدث أولاً

    @action(detail=False, methods=['get'])
    def last_order_status(self, request):
        """
        دالة API لجلب آخر طلب للمستخدم وإرجاع حالته فقط.
        """

        user_id = request.query_params.get('user', None)
        
        if not user_id:
            return Response({"detail": "User ID is required."}, status=400)

        # الحصول على آخر طلب للمستخدم بناءً على `user_id`
        last_order = Order.objects.filter(user_id=user_id).order_by('-order_date').first()
        
        if not last_order:
            return Response({"detail": "No orders found for this user."}, status=404)

        # إرجاع حالة الطلب فقط
        return Response({"order_status": last_order.status,"user":last_order.user.username})



class OrderItemView(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer_c

    # تغيير طريقة get_queryset لتكون بدون معلمات خارجية
    def get_queryset(self):
        # يتم تصفية البيانات داخل دالة get_order_items حسب المعلمات المرسلة
        return OrderItem.objects.all()

    # إجراء مخصص لإرجاع الأصناف الخاصة بالطلب
    @action(detail=False, methods=['get'])
    def get_order_items(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')
        user_id = request.query_params.get('user_id')

        # التحقق من وجود المعلمات المطلوبة
        if not order_id or not user_id:
            return Response({"detail": "Both 'order_id' and 'user_id' are required"}, status=400)
        
        # تصفية الأصناف بناءً على order_id و user_id
        items = self.get_queryset().filter(order__id=order_id, order__user_id=user_id)

        # إرجاع الأصناف باستخدام Serializer
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)



class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        delivery_profit = request.data.get('delivery_profit')
        _delivery_profit=0.0
        if delivery_profit is None:
            delivery_profit=0
        print("W"*90)
        # التحقق من الحالة الجديدة
        valid_statuses = [
            "pending",
            "courier_accepted",
            "courier_on_the_way",
            "picked_up_from_customer",
            "delivered_to_laundry",
            "in_progress",
            "ready_for_delivery",
            "completed",
            "canceled",
            "customer_accepted_end",
            "courier_accepted_end",
            "customer_received",
            "courier_received",
        ]
        user_id = request.data.get('user_id')
        sales_agent = SalesAgent.objects.get(user_id=user_id)


        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status update.'}, status=status.HTTP_400_BAD_REQUEST)

       # منع التحديث إذا كانت الحالة الحالية هي delivered_to_laundry
        if order.status == 'delivered_to_laundry':
            return Response({'error': 'Cannot change status from delivered_to_laundry.'}, status=status.HTTP_400_BAD_REQUEST)

        # if (order.status == 'picked_up_from_customer' and new_status == 'delivered_to_laundry'):
        #     _delivery_profit=float(delivery_profit)
        #     if _delivery_profit is None:
        #         _delivery_profit=0
        #     Transaction.objects.create(
        #         user_id=user_id,
        #         transaction_type='deposit',
        #         amount=_delivery_profit,
        #         debit=_delivery_profit,
        #         credit=0,
        #         description='ارباح توصيل مندوب'
        #     )
        # تحقق من الحالة الحالية قبل التحديث
        if (order.status == 'pending' and new_status == 'courier_accepted'):
            order.status = 'courier_accepted'
            order.sales_agent_id = sales_agent.id
           
        elif (order.status == 'courier_accepted' and new_status == 'courier_on_the_way'):
            order.status = 'courier_on_the_way'
        elif (order.status == 'courier_on_the_way' and new_status == 'picked_up_from_customer'):
            order.status = 'picked_up_from_customer'
        elif (order.status == 'picked_up_from_customer' and new_status == 'delivered_to_laundry'):
            order.status = 'delivered_to_laundry'
            _delivery_profit=delivery_profit
            _delivery_profit=Decimal(delivery_profit)
            if _delivery_profit is None:
                _delivery_profit=0
            Transaction.objects.create(
                user_id=user_id,
                transaction_type='deposit',
                amount=_delivery_profit,
                debit=_delivery_profit,
                credit=0,
                description='ارباح توصيل مندوب'
            )
             # إنشاء عملية مالية جديدة
            # Transaction.objects.create(
            #     user_id=user_id,
            #     transaction_type='deposit',
            #     amount=_delivery_profit,
            #     debit=_delivery_profit,
            #     credit=0,
            #     description='ارباح توصيل مندوب'
            # )
        else:
            return Response({'error': f'Status cannot be updated from {order.status} to {new_status}.'}, status=status.HTTP_400_BAD_REQUEST)
       
       
        try:
            SalesAgentOrder.objects.create(sales_agent=sales_agent, order=order,status=order.status,delivery_profit=_delivery_profit)

        except SalesAgent.DoesNotExist:
            return Response({'error': 'Sales agent not found.'}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)




class OrderStatusUpdateLaundryView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateLaundrySerializer

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        profit = order.total_amount
        _profit=0
        user_id = request.data.get('user_id')
        # التحقق من الحالة الجديدة
        valid_statuses = [
            'in_progress',
            'ready_for_delivery',
            'delivered_to_customer',
            'delivered_to_courier',
            'completed',
        ]

        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status update.'}, status=status.HTTP_400_BAD_REQUEST)

       # منع التحديث إذا كانت الحالة الحالية هي delivered_to_laundry
        if order.status == 'completed':
            return Response({'error': 'Cannot change status from completed.'}, status=status.HTTP_400_BAD_REQUEST)
        laundry = Laundry.objects.get(owner_id=user_id)
        sales_percentage = laundry.sales_percentage
        
        settings = Setting.objects.first()
        if settings:
            sales_percentage_setting=settings.sales_percentage
        if sales_percentage is None:
            sales_percentage=sales_percentage_setting
        # تحقق من الحالة الحالية قبل التحديث
        if (order.status == 'delivered_to_laundry' and new_status == 'in_progress'):
            order.status = 'in_progress'
        elif (order.status == 'in_progress' and new_status == 'ready_for_delivery'):
            order.status = 'ready_for_delivery'
        elif (order.status == 'ready_for_delivery' and new_status == 'delivered_to_customer'):
            order.status = 'delivered_to_customer'
        elif (order.status == 'delivered_to_customer' and new_status == 'completed'):
            order.status = 'completed'
            _profit=profit
            Transaction.objects.create(
                user_id=user_id,
                transaction_type='deposit',
                amount=order.total_amount-(order.total_amount*(sales_percentage/100)),
                debit=order.total_amount-(order.total_amount*(sales_percentage/100)),
                malaq_ratio=order.total_amount*(sales_percentage/100),
                credit=0,
                description='قيمة طلب معين'
            )
        elif (order.status == 'ready_for_delivery' and new_status == 'delivered_to_courier'):
            order.status = 'delivered_to_courier'
            _profit=profit
            Transaction.objects.create(
                user_id=user_id,
                transaction_type='deposit',
                amount=order.total_amount-(order.total_amount*(sales_percentage/100)),
                debit=order.total_amount-(order.total_amount*(sales_percentage/100)),
                malaq_ratio=order.total_amount*(sales_percentage/100),

                credit=0,
                description='قيمة طلب معين'
            )            
        else:
            return Response({'error': f'Status cannot be updated from {order.status} to {new_status}.'}, status=status.HTTP_400_BAD_REQUEST)
        # print("ddddddddddddddd"+str(order.laundry_id))
        # user_id = request.data.get('user_id')
        try:
            # sales_agent = SalesAgent.objects.get(user_id=user_id)
            LaundryOrder.objects.create(laundry_id=order.laundry_id, order=order,status=order.status,profit=_profit)

        except SalesAgent.DoesNotExist:
            return Response({'error': 'LaundryOrder not found.'}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailsView(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # تحديد الاستعلام الافتراضي
    serializer_class = OrderCustomSerializer  # تحديد الـ Serializer

    def get_queryset(self):
        # التصفية بناءً على `order_id` من الـ query params
        order_id = self.request.query_params.get('orderid', None)
        if order_id is not None:
            # إذا تم تقديم order_id، قم بتصفية النتائج ثم ترتيبها حسب الأحدث
            return Order.objects.filter(id=order_id).order_by('-order_date')  # ترتيب الأحدث أولاً
        return Order.objects.all().order_by('-order_date')  # ترتيب الأحدث أولاً
