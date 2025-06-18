from django.shortcuts import render, redirect

from orders.models import Order, SalesAgentOrder
from .forms import SalesAgentForm

def add_sales_agent(request):
    if request.method == 'POST':
        form = SalesAgentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # إعادة توجيه إلى صفحة النجاح أو الصفحة المطلوبة
    else:
        form = SalesAgentForm()
    
    return render(request, 'add_sales_agent.html', {'form': form})

def success(request):
    return render(request, 'success.html')



from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import SalesAgent
from .serializers import OrderAgentSerializer, SalesAgentOrderSerializer, SalesAgentSerializer

class SalesAgentOrderDetailView(generics.RetrieveAPIView):
    serializer_class = SalesAgentSerializer  # نستخدم Serializer المندوب مباشرةً
    queryset = SalesAgentOrder.objects.all()  # عدلنا إلى SalesAgentOrder

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            sales_agent_order = self.get_queryset().get(order__id=order_id)
            sales_agent = sales_agent_order.sales_agent
            
            # استخدام Serializer لتحويل بيانات المندوب إلى JSON
            serializer = self.get_serializer(sales_agent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SalesAgentOrder.DoesNotExist:
            return Response({'error': 'Sales agent order not found'}, status=status.HTTP_404_NOT_FOUND)





from .serializers import SalesAgentOrderSerializer

class SalesAgentOrdersByUserId(generics.ListAPIView):
    serializer_class = SalesAgentOrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # جلب المندوب بناءً على user_id
        try:
            sales_agent = SalesAgent.objects.get(user__id=user_id)
            return SalesAgentOrder.objects.filter(sales_agent=sales_agent)
        except SalesAgent.DoesNotExist:
            return SalesAgentOrder.objects.none()  # إرجاع قائمة فارغة إذا لم يتم العثور على المندوب
        


class SalesAgentOrderList(generics.ListAPIView):
    serializer_class = SalesAgentOrderSerializer

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return SalesAgentOrder.objects.filter(order_id=order_id)

from rest_framework.exceptions import ValidationError

from django.utils import timezone


class SalesAgentOrdersByDateRange(generics.ListAPIView):
    serializer_class = SalesAgentOrderSerializer

    def get_queryset(self):
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        user_id = self.kwargs['user_id']  # الحصول على رقم المستخدم من kwargs

        # تحويل التواريخ من النص إلى كائنات DateTime
        try:
            start_date = timezone.datetime.fromisoformat(start_date)
            end_date = timezone.datetime.fromisoformat(end_date)
        except ValueError:
            raise ValidationError("تاريخ غير صالح، يجب أن يكون بالتنسيق YYYY-MM-DD.")
        
        # محاولة الحصول على sales_agent
        sales_agent = SalesAgent.objects.filter(user_id=user_id).first()
        
        # إذا لم يوجد sales_agent، إرجاع مجموعة فارغة
        if not sales_agent:
            return SalesAgentOrder.objects.none()
        
        # فلترة الطلبات بناءً على تاريخ البدء والانتهاء ورقم المستخدم
        return SalesAgentOrder.objects.filter(
            assigned_date__range=(start_date, end_date),
            sales_agent=sales_agent
        )

class OrderAgentListView(generics.ListAPIView):
    serializer_class = OrderAgentSerializer

    def get_queryset(self):

      
        return Order.objects.filter(status__in=['pending', 'delivery_by_courier',])

from rest_framework import generics
class OrderAgentAcceptedListView(generics.ListAPIView):
    serializer_class = OrderAgentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        sales_agent = SalesAgent.objects.filter(user_id=user_id).first()
        
        if sales_agent:
            return Order.objects.filter(
                sales_agent_id=sales_agent.id,
                status__in=[
                    'courier_accepted',
                    'courier_on_the_way',
                    'picked_up_from_customer',
                    'courier_accepted_delivery',
                    'delivered_to_customer'
                ]
            )
        
        return Order.objects.none()  # إرجاع مجموعة فارغة