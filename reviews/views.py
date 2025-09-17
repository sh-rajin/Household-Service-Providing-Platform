from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer


# Create your views here.

class ReviewListCreateAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class ReviewDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None
        
    def get(self, request, pk):
        review = self.get_object(pk)
        
        if review:
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        return Response({'error': 'Review not found!'})
    
    def put(self, request, pk):
        review = self.get_object(pk)
        
        if review:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({'error': 'Review not found!'})
    
    
    def delete(self, request, pk):
        review = self.get_object(pk)
        
        if review:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)     
        return Response({'error': 'Review not found!'})
    
   
            
        
        
