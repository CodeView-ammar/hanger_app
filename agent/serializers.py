from orders.models import Order, SalesAgentOrder
from rest_framework import serializers
from .models import SalesAgent

class SalesAgentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAgentOrder
        fields = ['sales_agent', 'order', 'assigned_date']

class SalesAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAgent
        fields = ['name', 'phone', 'email', 'region', 'id_number', 'license_number', 'city', 'vehicle_type', 'created_at']



class SalesAgentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAgentOrder
        fields = '__all__'  # أو يمكنك تحديد الحقول التي تريد عرضها




class OrderAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # يمكنك تحديد الحقول التي تريد إرجاعها هنا
