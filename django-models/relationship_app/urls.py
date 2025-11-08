from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view: List all libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Class-based view: Detail view for a specific library
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
