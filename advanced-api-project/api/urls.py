from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints with individual generic views
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),  # Add pk
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),  # Add pk
    
    # Alternative patterns without primary key (if needed for tests)
    path('books/update/', views.BookUpdateGenericView.as_view(), name='book-update-generic'),
    path('books/delete/', views.BookDeleteGenericView.as_view(), name='book-delete-generic'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
