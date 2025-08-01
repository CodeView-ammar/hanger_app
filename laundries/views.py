from django.utils import timezone

from rest_framework.exceptions import ValidationError

from orders.models import LaundryOrder, Order
from rest_framework import viewsets
from services.models import LaundryService, Service
from settings.models import Setting
from .models import Laundry,LaundryHours
from .serializers import LaundryOrderSerializer,LaundryHoursSerializer, LaundrySerializer, LaundrySerializerUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserLaundryMark
from .serializers import UserLaundryMarkSerializer
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from .forms import LaundryForm
from users.models import Users
from django.contrib.auth.models import User

from rest_framework import generics

from django.db.models import DateField
from django.db.models.functions import Cast
from rest_framework import generics
from rest_framework.exceptions import ValidationError


class LaundryViewSet(viewsets.ModelViewSet):
    queryset = Laundry.objects.all()
    serializer_class = LaundrySerializer

    def list(self, request):
        search_query = request.query_params.get('search', None)
        if search_query:
            # استخدام البحث باستخدام %نصوص%
            queryset = self.queryset.filter(name__icontains=search_query , is_active=True )  # استبدل 'name' باسم الحقل الذي تريد البحث فيه
        else:
            queryset = self.queryset.filter(is_active=True ) 
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            laundry = self.get_object()  # Get the specific laundry instance
            serializer = self.get_serializer(laundry)
            return Response(serializer.data)  # Return the serialized data
        except Laundry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # Handle not found
        
class UserLaundryMarkViewSet(viewsets.ModelViewSet):
    queryset = UserLaundryMark.objects.all()
    serializer_class = UserLaundryMarkSerializer

    @action(detail=False, methods=['post'])
    def create_laundry_mark(self, request):
        # فحص البيانات التي تم استلامها
        print(f"Received data: {request.data}")

        user_id = request.data.get('user_id')
        laundry_id = request.data.get('laundry_id')

        if not user_id or not laundry_id:
            return Response({'error': 'user_id and laundry_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        # محاولة حفظ البيانات
        try:
            user = Users.objects.get(id=user_id)
            laundry = Laundry.objects.get(id=laundry_id)
            user_laundry_mark = UserLaundryMark(user=user, laundry=laundry)
            user_laundry_mark.save()
            return Response({'message': 'Laundry data saved successfully'}, status=status.HTTP_201_CREATED)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Laundry.DoesNotExist:
            return Response({'error': 'Laundry not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def user_laundry_mark_list(request):
    if request.method == 'GET':
        marks = UserLaundryMark.objects.all()
        serializer = UserLaundryMarkSerializer(marks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserLaundryMarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_laundry_mark_detail(request, pk):
    # استرجاع جميع العلامات الخاصة بالمستخدم
    marks = UserLaundryMark.objects.filter(user_id=pk)

    if not marks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)  # إذا لم توجد علامات، إرجاع 404

    serializer = UserLaundryMarkSerializer(marks, many=True)  # استخدم many=True
    return Response(serializer.data)  # إرجاع البيانات
   
@api_view(['DELETE'])  # يجب أن يكون نوع الطلب DELETE
def user_laundry_mark_delete(request, pk, laundry_id):
    try:
        mark = UserLaundryMark.objects.get(user_id=pk, laundry_id=laundry_id)
    except UserLaundryMark.DoesNotExist:
        return Response({'detail': 'User laundry mark not found.'}, status=status.HTTP_404_NOT_FOUND)

    mark.delete()
    return Response({'detail': 'User laundry mark deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)




def add_laundry(request):
    if request.method == 'POST':
        form = LaundryForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('E'*90)
            # Create the user first
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')

            # Create a new user instance
            # user = User(
            # )
            # user.save()  # حفظ المستخدم الجديد
            custom_user  = Users(
                name=name,
                username=phone,
                first_name=name,  # يمكنك استخدام الحقول المخصصة حسب الحاجة
                email=email,
                phone=phone,
                role='laundry_owner',
                password=phone,  # Hash the password
                is_active=False,  # Set to inactive initially
                is_laundry_owner=True
            )
            custom_user.set_password(phone)  # تعيين كلمة مرور (يجب تشفيرها)
            custom_user .save()  # Save the new user

            # Now create the laundry instance with the new user as the owner
            laundry = form.save(commit=False)  # Don't save yet
            laundry.owner = custom_user  # Set the owner to the new user
            laundry.owner_name = custom_user.username  # Optionally set the owner's name
            laundry.is_hidden = True  # Optionally set the owner's name
            laundry.is_active = False  # Optionally set the owner's name
            
            laundry.save()  # Now save the laundry instance
              # Add services only if they don't exist already
            services = Service.objects.all()
            for service in services:
                # Check if the LaundryService already exists
                if not LaundryService.objects.filter(laundry=laundry, service=service).exists():
                    LaundryService.objects.create(
                        laundry=laundry,  # Rely on the object instance
                        service=service
                    )
            
            return redirect('success')  # Redirect to the success page or required page
    else:
        form = LaundryForm()
    
    return render(request, 'add_laundry.html', {'form': form})






# from .models import LaundryService
# from .serializers import LaundryServiceSerializer

# class LaundryServiceViewSet(viewsets.ModelViewSet):
#     queryset = LaundryService.objects.all()
#     serializer_class = LaundryServiceSerializer




class LaundryListByUser(generics.ListAPIView):
    serializer_class = LaundrySerializerUser

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Laundry.objects.filter(owner_id=user_id)

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        laundries = self.get_queryset()
        if not laundries:
            return Response({'message': 'No laundries found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(laundries, many=True)
        return Response(serializer.data)



from rest_framework import generics
from .serializers import OrderLaundrySerializer
from orders.models import Order  # تأكد من أن المسار صحيح

class OrderLaundryListView(generics.ListAPIView):
    serializer_class = OrderLaundrySerializer

    def get_queryset(self):
        laundry_id = self.kwargs['laundry_id']

        return (
            Order.objects
            .select_related('user', 'payment_method')
            .prefetch_related('items', 'payment_details')
            .filter(
                laundry_id=laundry_id,
                status__in=[
                    'delivered_to_laundry',
                    'in_progress',
                    'ready_for_delivery',
                    'delivered_to_customer',
                ]
            )
        )
class LaundryOrdersByDateRange(generics.ListAPIView):
    serializer_class = LaundryOrderSerializer

    def get_queryset(self):
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        user_id = self.kwargs['user_id']  # الحصول على رقم المستخدم من kwargs

        # تحويل التواريخ من النص إلى كائنات DateTime
        try:
            start_date = timezone.datetime.fromisoformat(start_date)
            end_date = timezone.datetime.fromisoformat(end_date)
        except ValueError:
            raise ValidationError("تاريخ غير صالح، يجب أن يكون بالتنسيق YYYY-MM-DD.")
        laundry = Laundry.objects.get(owner_id=user_id)
        # فلترة الطلبات بناءً على تاريخ البدء والانتهاء ورقم المستخدم
        # return LaundryOrder.objects.filter(assigned_date__range=(start_date, end_date), laundry=laundry)
        return LaundryOrder.objects.filter(
            assigned_date__range=(start_date, end_date),
            laundry=laundry
        ).annotate(
            assigned_date_only=Cast('assigned_date', DateField())
        )



class LaundryHoursViewSet(viewsets.ModelViewSet):
    queryset = LaundryHours.objects.all()
    serializer_class = LaundryHoursSerializer

    @action(detail=False, methods=['get'], url_path='laundries/(?P<laundry_id>[^/.]+)/working-hours')
    def get_laundry_hours(self, request, laundry_id=None):
        hours = LaundryHours.objects.filter(laundry_id=laundry_id)
        serializer = self.get_serializer(hours, many=True)
        return Response(serializer.data)













