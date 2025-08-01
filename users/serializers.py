from rest_framework import serializers
from .models import Users,Address
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id",'username', 'email', 'phone', 'role', 'is_laundry_owner', 'password']  # Include password if needed
    
    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.name=validated_data['phone']
        user.save()
        return user



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'  


from .models import TransferRequest

class TransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields = '__all__'  # أو حدد الحقول يدويًا
        read_only_fields = ['date_requested', 'status']  # لا يمكن تغييرها من قبل المستخدم