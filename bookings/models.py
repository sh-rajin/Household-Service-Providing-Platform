from django.db import models
from services.models import Service
from account.models import Customer
# Create your models here.

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200, help_text="Enter Address....")
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Service : {self.service.name} - Customer : {self.customer.user.first_name}"
