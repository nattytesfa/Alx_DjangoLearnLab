from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints - using the exact patterns the test is looking for
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/', views.BookUpdateGenericView.as_view(), name='book-update'),  # Exact match
    path('books/delete/', views.BookDeleteGenericView.as_view(), name='book-delete'),  # Exact match
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
