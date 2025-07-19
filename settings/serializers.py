from rest_framework import serializers
from .models import SlideShowImage

class SlideShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShowImage
        fields = [
            'id',
            'image',
            'caption',
            'order', 'created_at', 'updated_at']


from .models import Setting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['key', 'sales_percentage', 'tax_rate', 'price_per_kg','price_per_kg_delivery']