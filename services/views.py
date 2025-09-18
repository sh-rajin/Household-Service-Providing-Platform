from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class ServiceListCreateAPIView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class ServiceDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return None
        
    def get(self, request, pk):
        service = self.get_object(pk)
        if service:
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        return Response({'error': 'Service not found!'})
    
    def put(self, request, pk):
        service = self.get_object(pk)
        if service:
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({'error': 'Service not found!'})
    
    def delete(self, request, pk):
        service = self.get_object(pk)
        if service:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Service not found!'})
            

class TopRatedServiceAPIView(APIView):
    def get(self, request):
        top_rated = Service.objects.filter(rating__gt=0).order_by('-rating')[:10]
        serializer = ServiceSerializer(top_rated, many=True)
        return Response(serializer.data)

