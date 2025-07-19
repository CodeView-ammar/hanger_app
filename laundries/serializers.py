from orders.models import LaundryOrder, Order
from rest_framework import serializers
from .models import Laundry,UserLaundryMark,LaundryHours

class LaundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laundry
        fields = ['id', 'owner', 'name', 'address', 'phone', 'email','image', 'created_at', 'updated_at','x_map','y_map', 'average_rating', 'total_reviews']
    
    def get_average_rating(self, obj):
        """حساب متوسط التقييم للمغسلة"""
        try:
            from reviews.models import LaundryReview
            reviews = LaundryReview.objects.filter(laundry=obj)
            if reviews.exists():
                total_rating = sum([review.rating for review in reviews])
                return round(total_rating / reviews.count(), 1)
            return 0
        except:
            return 0
    
    def get_total_reviews(self, obj):
        """عدد التقييمات الإجمالي"""
        try:
            from reviews.models import LaundryReview
            return LaundryReview.objects.filter(laundry=obj).count()
        except:
            return 0
    
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()


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

class LaundryHoursSerializer(serializers.ModelSerializer):
    # لإظهار التسمية العربية لليوم بدلاً من القيمة الانجليزية
    day_name_arabic = serializers.SerializerMethodField()

    class Meta:
        model = LaundryHours
        fields = ['id', 'day_of_week', 'day_name_arabic', 'opening_time', 'closing_time']

    def get_day_name_arabic(self, obj):
        # استرجاع التسمية العربية بناء على choices
        day_dict = dict(LaundryHours._meta.get_field('day_of_week').choices)
        return day_dict.get(obj.day_of_week, obj.day_of_week)