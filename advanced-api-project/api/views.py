from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .mixins import CustomCreateMixin, CustomUpdateMixin, CustomDestroyMixin
from .permissions import IsAuthenticatedOrReadOnly, IsAdminOrReadOnly


class BookListView(generics.ListAPIView):
        """
    Advanced Book List View with comprehensive query capabilities.
    
    IMPLEMENTATION DETAILS:
    
    FILTERING:
    - Uses DjangoFilterBackend for exact match filtering
    - Configured fields: publication_year, author
    - Supports multiple filter parameters combined
    
    SEARCHING:
    - Uses SearchFilter for text-based searching
    - Configured fields: title, author__name
    - Case-insensitive and supports partial matches
    - Uses Django's __icontains lookup
    
    ORDERING:
    - Uses OrderingFilter for sorting results
    - Configured fields: title, publication_year, author__name, id
    - Supports descending order with '-' prefix
    - Supports multiple field ordering
    
    CUSTOM FILTERING:
    - get_queryset method extended for custom range filtering
    - Additional parameters: min_year, max_year
    
    USAGE EXAMPLES:
    
    1. Filter books from specific year:
       GET /api/books/?publication_year=1997
    
    2. Search for books with 'potter' in title:
       GET /api/books/?search=potter
    
    3. Order books by publication year (newest first):
       GET /api/books/?ordering=-publication_year
    
    4. Combined query - search and filter:
       GET /api/books/?search=harry&publication_year=1997
    
    5. Multiple ordering:
       GET /api/books/?ordering=author__name,title
    
    6. Custom range filtering:
       GET /api/books/?min_year=1900&max_year=2000
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering configuration
    filterset_fields = ['publication_year', 'author']
    
    # Search configuration - search in multiple fields
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Enhanced queryset with additional filtering capabilities.
        This method can be extended for custom filtering logic.
        """
        queryset = super().get_queryset()
        
        # Example of custom filtering beyond DjangoFilterBackend
        # You can add custom query parameters here
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
            
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by its ID.
    
    Features:
    - Public access
    - Returns detailed book information including author
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(CustomCreateMixin, generics.CreateAPIView):
    """
    Create a new book instance with enhanced response format.
    
    Features:
    - Requires authentication
    - Custom response format with status and message
    - Validation for publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Customize the creation process if needed.
        This hook is called after validation but before saving.
        """
        serializer.save()
        # You could add additional logic here, like logging or notifications

class BookViewSet(generics.GenericAPIView):
    """
    Comprehensive viewset demonstrating multiple HTTP methods in one class.
    This is an alternative approach to individual generic views.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk=None):
        """
        Handle GET requests - list all books or retrieve single book.
        """
        if pk:
            # Retrieve single book
            book = self.get_object()
            serializer = self.get_serializer(book)
            return Response(serializer.data)
        else:
            # List all books
            books = self.get_queryset()
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        """
        Handle POST requests - create new book.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        """
        Handle PUT requests - update entire book.
        """
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request, pk):
        """
        Handle PATCH requests - partial update of book.
        """
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests - remove book.
        """
        book = self.get_object()
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookUpdateView(CustomUpdateMixin, generics.UpdateAPIView):
    """
    Update an existing book instance with enhanced response format.
    
    Features:
    - Requires authentication
    - Custom response format
    - Supports partial updates
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Customize the update process if needed.
        """
        serializer.save()
        # Additional logic can be added here


class BookDeleteView(CustomDestroyMixin, generics.DestroyAPIView):
    """
    Delete a book instance with enhanced response format.
    
    Features:
    - Requires authentication
    - Custom response format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        """
        Customize the deletion process if needed.
        """
        # You could add logging or cleanup logic here
        instance.delete()


class AuthorListView(generics.ListAPIView):
    """
    List all authors with their books.
    
    Features:
    - Public access
    - Includes nested book data
    - Search by author name
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single author by ID with their books.
    
    Features:
    - Public access
    - Returns author details with nested books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
