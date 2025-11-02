from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ['title', 'author', 'publication_year']
    
    # Add filters for author and publication year
    list_filter = ['author', 'publication_year']
    
    # Enable search by title and author
    search_fields = ['title', 'author']
    
    # Order by publication year (newest first) by default
    ordering = ['-publication_year']
