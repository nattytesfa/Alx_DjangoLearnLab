from django.urls import path
from .views import list_books, LibraryDetailView, LibraryListView  

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view: List all libraries
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    
    # Class-based view: Detail view for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
