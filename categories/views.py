from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Category
from .serializers import CategorySerializer


# Create your views here.

class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None
        
    def get(self, request, pk):
        category = self.get_object(pk)
        
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    

    def put(self, request, pk):
        category = self.get_object(pk)
        
        if category:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
        return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    
