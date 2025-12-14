from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserPostsView, UserFeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:username>/posts/', UserPostsView.as_view(), name='user-posts'),
    path('feed/', UserFeedView.as_view(), name='user-feed'),
]
