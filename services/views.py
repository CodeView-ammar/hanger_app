from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer
from django_filters import rest_framework as filters

class ServiceFilter(filters.FilterSet):
    laundry_id = filters.NumberFilter(field_name='laundry_id')

    class Meta:
        model = Service
        fields = ['laundry_id']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ServiceFilter