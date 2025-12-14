from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer

User = get_user_model()


class FollowUserView(APIView):
    """View for following a user."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """Follow a user."""
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Prevent following yourself
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.is_following(user_to_follow):
            return Response(
                {'error': 'You are already following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following list
        request.user.following.add(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}.',
            'user': UserProfileSerializer(user_to_follow).data,
            'following_count': request.user.following_count,
            'follower_count': user_to_follow.follower_count,
        }, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """View for unfollowing a user."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """Unfollow a user."""
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # Check if actually following
        if not request.user.is_following(user_to_unfollow):
            return Response(
                {'error': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove from following list
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}.',
            'user': UserProfileSerializer(user_to_unfollow).data,
            'following_count': request.user.following_count,
            'follower_count': user_to_unfollow.follower_count,
        }, status=status.HTTP_200_OK)


class ToggleFollowView(APIView):
    """View to toggle follow/unfollow a user."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """Toggle follow/unfollow a user."""
        target_user = get_object_or_404(User, id=user_id)
        
        # Prevent following yourself
        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Toggle follow status
        if request.user.is_following(target_user):
            request.user.following.remove(target_user)
            action = 'unfollowed'
        else:
            request.user.following.add(target_user)
            action = 'followed'
        
        return Response({
            'action': action,
            'message': f'You have {action} {target_user.username}.',
            'is_following': request.user.is_following(target_user),
            'user': UserProfileSerializer(target_user).data,
            'following_count': request.user.following_count,
            'follower_count': target_user.follower_count,
        }, status=status.HTTP_200_OK)


class FollowersListView(generics.ListAPIView):
    """View to list followers of a user."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.followers.all()


class FollowingListView(generics.ListAPIView):
    """View to list users that a user is following."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.following.all()


class CheckFollowStatusView(APIView):
    """View to check follow status between users."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        """Check if current user is following the target user."""
        target_user = get_object_or_404(User, id=user_id)
        
        return Response({
            'is_following': request.user.is_following(target_user),
            'is_followed_by': target_user.is_following(request.user),
            'user': UserProfileSerializer(target_user).data,
        }, status=status.HTTP_200_OK)
