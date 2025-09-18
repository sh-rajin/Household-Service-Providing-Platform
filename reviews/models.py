from django.db import models
from services.models import Service
from account.models import User
from django.core.validators import MaxValueValidator
# Create your models here.

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # প্রথমে review save হবে

        # Service-এর rating ও review_count update
        service = self.service
        reviews = service.reviews.all()
        service.review_count = reviews.count()
        service.rating = sum(r.rating for r in reviews) / reviews.count()
        service.save()

    def __str__(self):
        return f'Review by {self.user.username} for {self.service.name}'
