from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, LibraryListView, register, add_book, edit_book, delete_book

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Permission-secured Book URLs
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
    
    # Existing URLs
    path('books/', list_books, name='list_books'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
