from django.urls import path, include
from .views import ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail')
]