from django.urls import path
from .views import list_books, LibraryDetailView, LibraryListView, register_view, login_view, logout_view

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Existing URLs
    path('books/', list_books, name='list_books'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
