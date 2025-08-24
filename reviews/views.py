from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from reviews.models import LaundryReview
from .serializers import LaundryReviewSerializer, LaundryReviewCreateSerializer
from laundries.models import Laundry
from rest_framework.views import APIView

class LaundryReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = LaundryReviewCreateSerializer
    permission_classes = []  # معطل للاختبار
    
    def get_queryset(self):
        laundry_id = self.kwargs.get('laundry_id')
        if laundry_id:
            return LaundryReview.objects.filter(laundry_id=laundry_id)
        return LaundryReview.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LaundryReviewCreateSerializer
        return LaundryReviewSerializer
    
    def perform_create(self, serializer):
        # استخدام البيانات المرسلة مباشرة للاختبار
        service_quality = self.request.data.get('service_quality')
        delivery_speed = self.request.data.get('delivery_speed')
        price_value = self.request.data.get('price_value')

        try:
            avg_rating = round((
                int(service_quality) +
                int(delivery_speed) +
                int(price_value)
            ) / 3)
        except Exception:
            avg_rating = 5  # fallback افتراضي
        serializer.save(rating=avg_rating)

class CheckOrderReviewView(APIView):
    def get(self, request, order_id, user_id):
        reviewed = LaundryReview.is_order_reviewed(user_id=user_id, order_id=order_id)
        return Response({"reviewed": reviewed}, status=status.HTTP_200_OK)


class LaundryReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LaundryReview.objects.all()
    serializer_class = LaundryReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        laundry_id = self.kwargs.get('laundry_id')
        if laundry_id:
            return LaundryReview.objects.filter(laundry_id=laundry_id)
        return LaundryReview.objects.all()

@api_view(['GET'])
def laundry_rating_stats(request, laundry_id):
    """إحصائيات تقييم المغسلة"""
    try:
        laundry = Laundry.objects.get(id=laundry_id)
        reviews = LaundryReview.objects.filter(laundry=laundry)
        
        if not reviews.exists():
            return Response({
                'average_rating': 0,
                'total_reviews': 0,
                'rating_breakdown': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'average_service_quality': 0,
                'average_delivery_speed': 0,
                'average_price_value': 0
            })
        
        stats = reviews.aggregate(
            avg_rating=Avg('rating'),
            avg_service_quality=Avg('service_quality'),
            avg_delivery_speed=Avg('delivery_speed'),
            avg_price_value=Avg('price_value')
        )
        
        # تفكيك التقييمات
        rating_breakdown = {}
        for i in range(1, 6):
            rating_breakdown[i] = reviews.filter(rating=i).count()
        
        return Response({
            'average_rating': round(stats['avg_rating'], 1) if stats['avg_rating'] else 0,
            'total_reviews': reviews.count(),
            'rating_breakdown': rating_breakdown,
            'average_service_quality': round(stats['avg_service_quality'], 1) if stats['avg_service_quality'] else 0,
            'average_delivery_speed': round(stats['avg_delivery_speed'], 1) if stats['avg_delivery_speed'] else 0,
            'average_price_value': round(stats['avg_price_value'], 1) if stats['avg_price_value'] else 0
        })
        
    except Laundry.DoesNotExist:
        return Response({'error': 'المغسلة غير موجودة'}, status=status.HTTP_404_NOT_FOUND)


