from django.urls import path, include
from .views import ServiceListCreateAPIView, ServiceDetailAPIView, TopRatedServiceAPIView

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='service-list'),
    path('<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('top-rated/', TopRatedServiceAPIView.as_view(), name='top-service')
]