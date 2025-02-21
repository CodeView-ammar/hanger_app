from .models import Users,Address

from .serializers import UsersSerializer,AddressSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [IsAuthenticated]  # Change this if needed
    def retrieve(self, request, *args, **kwargs):
        phone = request.query_params.get('phone', None)  # استخرج رقم الجوال من المعلمات
        if phone is not None:
            try:
                user = Users.objects.get(phone=phone)  # ابحث عن المستخدم باستخدام رقم الجوال
                return Response({'id': user.id}, status=status.HTTP_200_OK)  # إرجاع الـ id
            except Users.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'detail': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_phone(request, phone):
    # استرجاع جميع العلامات الخاصة بالمستخدم
    marks = Users.objects.filter(phone=phone)

    if not marks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)  # إذا لم توجد علامات، إرجاع 404

    serializer = UsersSerializer(marks, many=True)  # استخدم many=True
    return Response(serializer.data)  # إرجاع البيانات
   


@api_view(['GET'])
def user_phone_login(request, phone):
    try:
        user = Users.objects.get(phone=phone,is_active=True)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
from django.shortcuts import render

def user_management(request):
    return render(request, 'users/user_management.html')



from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Address
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def create(self, request):
        # استخراج بيانات الإحداثيات والعنوان
        user = request.data.get('user')
        
        # التحقق إذا كان العنوان موجود بالفعل بناءً على الإحداثيات
        try:
            address = Address.objects.get(user_id=user)
            # إذا كان موجودًا، نقوم بتحديثه
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            # إذا لم يكن موجودًا، نقوم بإنشاء سجل جديد
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            address = Address.objects.get(pk=pk)
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            address = Address.objects.get(pk=pk)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            address = Address.objects.get(pk=pk)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
class AddressDetailView(APIView):
    def get(self, request, user_id):
        try:
            address = Address.objects.get(user_id=user_id)
            serializer = AddressSerializer(address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)