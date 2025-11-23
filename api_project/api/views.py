from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
