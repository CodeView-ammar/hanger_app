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



class OrderLaundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # يمكنك تحديد الحقول التي تريد إرجاعها هنا



class LaundryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryOrder
        fields = '__all__'  # أو يمكنك تحديد الحقول التي تريد عرضها