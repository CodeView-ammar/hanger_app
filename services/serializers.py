from rest_framework import serializers
from .models import Service,ServiceCategory, SubService

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class LaundryServiceSerializer(serializers.ModelSerializer):
    """Maintains compatibility with existing API structure"""
    service = ServiceSerializer(source='*')
    laundry = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'laundry', 'service']



class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'
