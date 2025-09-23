from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CustomerListAPIView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        data = []
        for customer in customers:
            data.append({
                'username': customer.user.username,
                'first_name': customer.user.first_name,
                'last_name': customer.user.last_name,
                'email': customer.user.email,
                'phone': customer.phone,
                'address': customer.address
            })
        return Response(data)

class CustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            data = {
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': customer.phone,
                'address': customer.address
            }
            return Response(data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)
        
    def put(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            user = request.user
            user.username = request.data.get('username', user.username)
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            customer.phone = request.data.get('phone', customer.phone)  
            customer.address = request.data.get('address', customer.address)
            user.save()
            customer.save()
            return Response({'message': 'Profile updated successfully'})
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)
            
            