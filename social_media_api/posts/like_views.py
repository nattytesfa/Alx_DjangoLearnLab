from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Like
from .serializers import LikeSerializer
from notifications.models import Notification

User = get_user_model()


class LikePostView(APIView):
    """View for liking a post."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Like a post."""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        like = Like.objects.create(user=user, post=post)
        
        # Create notification (if user is not liking their own post)
        if user != post.author:
            Notification.create_like_notification(
                recipient=post.author,
                actor=user,
                post=post
            )
        
        return Response({
            'message': 'Post liked successfully.',
            'like': LikeSerializer(like).data,
            'like_count': post.like_count,
            'is_liked': True
        }, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """View for unliking a post."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Unlike a post."""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if liked
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete like
        like.delete()
        
        return Response({
            'message': 'Post unliked successfully.',
            'like_count': post.like_count,
            'is_liked': False
        }, status=status.HTTP_200_OK)


class ToggleLikeView(APIView):
    """View to toggle like/unlike a post."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Toggle like/unlike a post."""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if already liked
        like = Like.objects.filter(user=user, post=post).first()
        
        if like:
            # Unlike
            like.delete()
            action = 'unliked'
            is_liked = False
        else:
            # Like
            like = Like.objects.create(user=user, post=post)
            
            # Create notification (if user is not liking their own post)
            if user != post.author:
                Notification.create_like_notification(
                    recipient=post.author,
                    actor=user,
                    post=post
                )
            
            action = 'liked'
            is_liked = True
        
        return Response({
            'action': action,
            'message': f'Post {action} successfully.',
            'is_liked': is_liked,
            'like_count': post.like_count
        }, status=status.HTTP_200_OK)


class PostLikesListView(APIView):
    """View to list users who liked a post."""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        """Get list of users who liked a post."""
        post = get_object_or_404(Post, pk=pk)
        likes = post.likes.all()
        
        # Paginate if needed
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = LikeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
