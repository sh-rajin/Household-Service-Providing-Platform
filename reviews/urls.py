from django.urls import path, include
from .views import ReviewDetailAPIView, ReviewListAPIView

urlpatterns = [
    path('', ReviewListAPIView.as_view(), name='review-list'),
    # path('', ServiceReviewCreateAPIView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail')
]