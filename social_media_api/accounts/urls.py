from django.urls import path
from . import views
from .follow_views import (
    FollowUserView, UnfollowUserView, ToggleFollowView,
    FollowersListView, FollowingListView, CheckFollowStatusView
)

urlpatterns = [

    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    
    # User listing endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user-detail'),

    # Follow management endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('toggle-follow/<int:user_id>/', ToggleFollowView.as_view(), name='toggle-follow'),
    path('check-follow/<int:user_id>/', CheckFollowStatusView.as_view(), name='check-follow-status'),
    
    # Followers/Following lists
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='user-following'),
]
