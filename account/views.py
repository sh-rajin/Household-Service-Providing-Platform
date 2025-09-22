from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token 
from customer.models import Customer
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, LoginSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
# Create your views here.

   
    
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Customer.objects.create(
                user=user,
                phone = request.data.get('phone'),
                address = request.data.get('address')
            )
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'http://127.0.0.1:8000/api/activate/{uid}/{token}/'
            email_subject = 'Activate your account'
            email_body = render_to_string('account/activation.html',{'Confirm_Email': confirm_link})
            email = EmailMultiAlternatives(email_subject,"", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({'message': 'User registered successfully. Please check your email to activate your account.'}, status=201)
        return Response(serializer.errors, status=400)
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(f"uid : {uid}")
        print(f'user : {user}')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Account activated successfully")
    else:
        return HttpResponse("Activation link is invalid", status=400)
    
        
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # print(f"{email} ---- {password}")
            user = authenticate(request, email=email, password=password)
            # print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,'user_id' : user.id, 'role' : user.role},status=200)
                return Response({'error': 'Account is not activated. Please check your email.'}, status=403)
            return Response({'error': 'Invalid credentials'}, status=401)
        else:
            return Response(serializer.errors, status=400)
        

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        self.request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Account Logout successfully"})
    
    
    
class Customer(APIView):
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

            
            
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not user.check_password(old_password):
            return Response({'error' : "Old Password is incorrect"}, status=400)
        
        if new_password != confirm_password:
            return Response({'error' : "New Password and Confirm Password do not match"}, status=400)
        
        user.set_password(new_password)
        user.save()
        return Response({'message' : "Password changed successfully"})
    
    