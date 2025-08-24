from rest_framework import serializers
from .models import  LaundryReview
from users.serializers import UsersSerializer

# class ServiceReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceReview
#         fields = '__all__'

class LaundryReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = LaundryReview
        fields = [
            'id', 'laundry', 'user', 'user_name', 'rating', 'comment',
            'service_quality', 'delivery_speed', 'price_value',
            'average_rating', 'created_at', 'updated_at'
        ]
        # read_only_fields = [ 'created_at', 'updated_at']

class LaundryReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryReview
        fields = [
            'laundry','user',"order", 'rating', 'comment', 'service_quality', 
            'delivery_speed', 'price_value'
        ]
        read_only_fields = ['rating']  # rating يتم حسابه تلقائيًا

    
    # def create(self, validated_data):
    #     # إضافة المستخدم الحالي من السياق

    #     return super().create(validated_data)