from rest_framework import viewsets
from .models import Service, ServiceCategory, SubService
from .serializers import LaundryServiceSerializer, ServiceSerializer,ServiceCategorySerializer, SubServiceSerializer
from django_filters import rest_framework as filters

class ServiceFilter(filters.FilterSet):
    laundry_id = filters.NumberFilter(field_name='laundry_id')
    category = filters.NumberFilter(field_name='category')

    class Meta:
        model = Service
        fields = ['laundry_id',"category"]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ServiceFilter







class LaundryServiceFilter(filters.FilterSet):
    laundry_id = filters.NumberFilter(field_name='laundry_id')
    category = filters.NumberFilter(field_name='category')

    class Meta:
        model = Service
        fields = ['laundry_id', "category"]


class LaundryServiceViewSet(viewsets.ModelViewSet):
    """Maintains compatibility with existing LaundryService API by using Service model directly"""
    queryset = Service.objects.all()
    serializer_class = LaundryServiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LaundryServiceFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        laundry_id = self.request.query_params.get('laundry_id', None)
        category = self.request.query_params.get('category', None)

        if laundry_id:
            queryset = queryset.filter(laundry_id=laundry_id)

        if category:
            queryset = queryset.filter(category=category)

        return queryset


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceCategorySerializer
    queryset = ServiceCategory.objects.all()  # تأكد من تحديد queryset هنا

    def get_queryset(self):
        laundry_id = self.request.query_params.get('laundry_id', None)
        if laundry_id is not None:
            # تصفية التصنيفات بناءً على وجود خدمات مرتبطة بـ laundry_id مباشرة
            return ServiceCategory.objects.filter(services__laundry_id=laundry_id).distinct()
        return ServiceCategory.objects.all() 


class SubServiceViewSet(viewsets.ModelViewSet):
    serializer_class = SubServiceSerializer

    def get_queryset(self):
        LaundryService_id = self.request.query_params.get('LaundryService_id')
        if LaundryService_id is not None:
            return SubService.objects.filter(service_id=LaundryService_id)
        return SubService.objects.none()

