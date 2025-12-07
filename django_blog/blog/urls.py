from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    UserRegisterView,
    UserProfileView
)

urlpatterns = [
    # Home and blog URLs
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    
    # Authentication URLs
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/logout.html',
        next_page='home'
    ), name='logout'),
    

    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Profile URL
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Password change URLs (Django built-in)
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='blog/password_change.html'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='blog/password_change_done.html'
    ), name='password_change_done'),
]
