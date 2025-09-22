from django.urls import path
from .views import CustomerAPIView, CustomerListAPIView

urlpatterns = [
    path('', CustomerListAPIView.as_view(), name='customer'),
    path('profile/', CustomerAPIView.as_view(), name='customer-profile'),
]