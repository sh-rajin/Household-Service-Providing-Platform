from rest_framework import serializers
from .models import Customer, User

# class CustomerSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Customer
#         fields = '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email','phone')
        
    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        phone = self.validated_data['phone']
        
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username is already taken.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email is already registered.'})
        
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role = "customer",
            phone = phone
        )
        
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        
        