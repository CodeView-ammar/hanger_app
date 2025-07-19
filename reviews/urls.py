from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'service-reviews', views.ServiceReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('laundry/<int:laundry_id>/reviews/', views.LaundryReviewListCreateView.as_view(), name='laundry-reviews'),
    path('laundry/<int:laundry_id>/stats/', views.laundry_rating_stats, name='laundry-rating-stats'),
    path('review/<int:pk>/', views.LaundryReviewDetailView.as_view(), name='review-detail'),
    
    path('reviews/laundry/<int:laundry_id>/reviews/', views.LaundryReviewListCreateView.as_view(), name='laundry-reviews'),
    path('reviews/laundry/<int:laundry_id>/stats/', views.laundry_rating_stats, name='laundry-review-stats'),

]