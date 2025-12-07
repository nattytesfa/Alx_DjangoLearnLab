from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .comment_views import (
    CommentCreateView, 
    CommentUpdateView, 
    CommentDeleteView,
    comment_reply_view,
    toggle_comment_approval
)
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    UserRegisterView,
    UserProfileView,
    PostSearchView,          
    PostByTagListView  
)

urlpatterns = [
    # Home and blog URLs
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    


# Search and Tag URLs - MUST BE ADDED HERE
path('search/', PostSearchView.as_view(), name='post-search'),
path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tag-posts'),
    # Comment URLs

    path('post/<int:pk>/comments/new/',  
         CommentCreateView.as_view(), 
         name='comment-create'),
    path('comment/<int:pk>/update/',  
         CommentUpdateView.as_view(), 
         name='comment-update'),
    path('post/<int:post_id>/comment/<int:parent_id>/reply/', 
         comment_reply_view, 
         name='comment-reply'),
    path('comment/<int:pk>/edit/', 
         CommentUpdateView.as_view(), 
         name='comment-edit'),
    path('comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment-delete'),
    path('comment/<int:comment_id>/toggle-approval/', 
         toggle_comment_approval, 
         name='toggle-comment-approval'),
    
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
    
    # Profile URL
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Password change URLs
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='blog/password_change.html'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='blog/password_change_done.html'
    ), name='password_change_done'),
]
