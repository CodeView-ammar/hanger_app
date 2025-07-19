from rest_framework import serializers
from .models import ServiceReview, LaundryReview
from users.serializers import UsersSerializer

class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = '__all__'

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
        read_only_fields = ['user', 'created_at', 'updated_at']

class LaundryReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryReview
        fields = [
            'laundry', 'rating', 'comment', 'service_quality', 
            'delivery_speed', 'price_value'
        ]
    
    def create(self, validated_data):
        # إضافة المستخدم الحالي من السياق
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)