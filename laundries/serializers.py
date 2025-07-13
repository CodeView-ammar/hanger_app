from orders.models import LaundryOrder, Order
from rest_framework import serializers
from .models import Laundry,UserLaundryMark

class LaundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laundry
        fields = ['id', 'owner', 'name', 'address', 'phone', 'email','image', 'created_at', 'updated_at','x_map','y_map']


class UserLaundryMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLaundryMark
        fields = '__all__'


# from .models import LaundryService

# class LaundryServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LaundryService
#         fields = '__all__'  # يمكنك تحديد الحقول التي تريد تضمينها

from .models import Laundry
class LaundrySerializerUser(serializers.ModelSerializer):
    class Meta:
        model = Laundry
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'email',
            'image',
            'membership_start_date',
            'membership_end_date',
            'sales_percentage',
            'is_active',
            'created_at',
            'updated_at',
        ]



# class OrderLaundrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'  # يمكنك تحديد الحقول التي تريد إرجاعها هنا



class LaundryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryOrder
        fields = '__all__'  # أو يمكنك تحديد الحقول التي تريد عرضها




from rest_framework import serializers
from orders.models import Order, OrderItem
from users.models import Users, Address
from users.serializers import UsersSerializer  # تأكد من وجود هذا السيريالايزر أو أنشئه
from services.serializers import ServiceSerializer  # لعناصر الطلب


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'service', 'service_type', 'quantity', 'price', 'notes']


class OrderLaundrySerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    address = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'  # أو حدد الحقول المطلوبة بشكل يدوي

    def get_address(self, obj):
        address = Address.objects.filter(user=obj.user).first()
        return AddressSerializer(address).data if address else None
