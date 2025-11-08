"""
Sample queries demonstrating complex relationships in Django ORM
"""

def get_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    from .models import Author, Book
    
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def get_books_in_library(library_name):
    """
    List all books in a specific library
    """
    from .models import Library
    
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Library.books.model.objects.none()

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library
    """
    from .models import Library
    
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Library.librarian.RelatedObjectDoesNotExist:
        return None

# Example usage and testing
if __name__ == "__main__":
    import os
    import django
    from django.conf import settings
    
    # Setup Django environment
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
        django.setup()
    
    # Test the queries
    print("=== Testing Relationship Queries ===")
    
    # Test query 1: Books by author
    print("\n1. Books by a specific author:")
    books = get_books_by_author("Sample Author")
    for book in books:
        print(f"   - {book.title}")
    
    # Test query 2: Books in library
    print("\n2. Books in a specific library:")
    library_books = get_books_in_library("Sample Library")
    for book in library_books:
        print(f"   - {book.title}")
    
    # Test query 3: Librarian for library
    print("\n3. Librarian for a specific library:")
    librarian = get_librarian_for_library("Sample Library")
    if librarian:
        print(f"   - {librarian.name}")
    else:
        print("   - No librarian found")
