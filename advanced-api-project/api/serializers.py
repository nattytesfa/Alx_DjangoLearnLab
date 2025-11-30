from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with custom validation.
    
    Handles serialization of:
    - id (auto-generated)
    - title
    - publication_year
    - author (foreign key)
    
    Validation:
    - Custom validation for publication_year to ensure it's not in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Validate that publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested Book serialization.
    
    Handles serialization of:
    - id (auto-generated)
    - name
    - books (nested serialization of related Book objects)
    
    Nested Relationships:
    - Uses BookSerializer to serialize all books by this author
    - The 'books' field comes from the related_name in the Book model's ForeignKey
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']


class AuthorBookCreateSerializer(serializers.ModelSerializer):
    """
    Alternative serializer for creating authors with books in a single request.
    
    This demonstrates handling nested creation, though for simplicity
    we'll keep books as read-only in the main AuthorSerializer.
    """
    books = BookSerializer(many=True, required=False)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def create(self, validated_data):
        """
        Custom create method to handle nested book creation.
        This is an advanced feature for demonstration.
        """
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author
