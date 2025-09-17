from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    ROLE_CHOICES =(
        ("customer" , "Customer"),   
        ("provider" , "Provider"),
        ("admin" , "Admin") 
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=11, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f'{self.username} - {self.role}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to="account/images/")
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'