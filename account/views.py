from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token 
from .models import Customer, User
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
            customer = Customer.objects.create(
                user=user,
                address = request.data.get('address'),
                image = request.data.get('image')
            )
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'http://127.0.0.1:8000/account/activate/{uid}/{token}/'
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
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        Response({"message": "Account activated successfully"})
    
        
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,'user_id' : user.id, 'role' : user.role},status=200)
                return Response({'error': 'Account is not activated. Please check your email.'}, status=403)
            return Response(serializer.errors, status=403)
        

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        self.request.user.auth_token.delete()
        logout(request)
        Response({"message": "Account Logout successfully"})