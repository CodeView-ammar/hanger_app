from rest_framework import serializers
from .models import LaundryService, Service,ServiceCategory, SubService

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class LaundryServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = LaundryService
        fields = '__all__'



class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'
