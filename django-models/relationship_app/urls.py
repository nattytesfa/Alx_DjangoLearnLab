from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, LibraryListView, register, admin_view, librarian_view, member_view

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Role-based view URLs
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    
    # Existing URLs
    path('books/', list_books, name='list_books'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
