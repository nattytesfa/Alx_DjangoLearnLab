"""
Authentication and Permissions Setup:

1. Token Authentication:
   - Users obtain tokens via /api/auth-token/
   - Include token in header: Authorization: Token <your_token>
   
2. Permission Classes:
   - BookList: AllowAny - Anyone can view books
   - BookViewSet: 
        - list/retrieve: AllowAny - Anyone can view
        - create/update/delete: IsAuthenticated - Only authenticated users
   
3. Testing:
   - Without token: Can view books but cannot modify
   - With token: Full CRUD access (based on user permissions)
"""

from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books
    Allow any user to view books (read-only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Anyone can view books

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy
    Requires authentication for all operations except listing
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any user to view books (list and retrieve)
            permission_classes = [AllowAny]
        else:
            # Require authentication for create, update, delete
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
