from rest_framework import serializers
from .models import Cart, LaundryOrder, PaymentMethodsDetails, Service,PaymentMethod

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']  # تأكد من تضمين الحقول المطلوبة

class CartSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()  # حقل لاسم الخدمة

    class Meta:
        model = Cart
        fields = ['id', 'user', 'laundry', 'service', 'price', 'quantity', 'service_name',"service_type"]  # تأكد من تضمين service_name هنا

    def get_service_name(self, obj):
        try:
            return obj.service.name  # استرجاع اسم الخدمة المرتبطة
        except Service.DoesNotExist:
            return None  # إذا لم توجد الخدمة، قم بإرجاع None


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'  # تأكد من تضمين الحقول المطلوبة

class PaymentMethodsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodsDetails
        fields = '__all__'  # تأكد من تضمين الحقول المطلوبة




from .models import Order, OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'  # or specify fields explicitly


class OrderItemSerializer_c(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['service_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Ensure this is set

    class Meta:
        model = Order
        fields = ['id','user','laundry','order_date','total_amount','status','pickup_date','delivery_date','payment_status','payment_method','items','delivery_method','delegate_note','sales_agent'] 

class OrderCustomSerializer(serializers.ModelSerializer):
    # إضافة اسم المغسلة
    laundry_id = serializers.CharField(source='laundry.id', read_only=True)
    laundry_name = serializers.CharField(source='laundry.name', read_only=True)
    laundry_address = serializers.CharField(source='laundry.address', read_only=True)
    laundry_x_map = serializers.CharField(source='laundry.x_map', read_only=True)
    laundry_y_map = serializers.CharField(source='laundry.y_map', read_only=True)
    laundry_phone = serializers.CharField(source='laundry.phone', read_only=True)
    
    # إضافة صورة المغسلة
    laundry_image = serializers.ImageField(source='laundry.image', read_only=True)
    # إضافة حالة الطلب
    status = serializers.CharField(read_only=True)
    # إضافة إجمالي الطلب
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # إضافة تاريخ الطلب
    order_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['id',"laundry_id",'laundry_name', 'laundry_image','laundry_address','laundry_x_map','laundry_y_map','laundry_phone', 'total_amount', 'order_date', 'status']
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderStatusUpdateLaundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
