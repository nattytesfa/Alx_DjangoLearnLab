from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserPostsView, UserFeedView
from .like_views import LikePostView, UnlikePostView, ToggleLikeView, PostLikesListView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:username>/posts/', UserPostsView.as_view(), name='user-posts'),
    path('feed/', UserFeedView.as_view(), name='user-feed'),
    
    # Like endpoints
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('posts/<int:pk>/toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('posts/<int:pk>/likes/', PostLikesListView.as_view(), name='post-likes'),
]
