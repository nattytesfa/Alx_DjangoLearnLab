from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Notification
from .serializers import (
    NotificationSerializer, 
    NotificationUpdateSerializer,
    MarkAllAsReadSerializer
)

User = get_user_model()


class NotificationViewSet(GenericViewSet):
    """
    ViewSet for managing notifications.
    """
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the current user."""
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)
        
        # Filter by read status if provided
        read_status = self.request.query_params.get('read')
        if read_status is not None:
            queryset = queryset.filter(read=(read_status.lower() == 'true'))
        
        # Filter by notification type if provided
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        return queryset.order_by('-created_at')
    
    def list(self, request):
        """List all notifications for the current user."""
        queryset = self.get_queryset()
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications."""
        unread_notifications = self.get_queryset().filter(read=False)
        
        # Count unread notifications
        unread_count = unread_notifications.count()
        
        # Get recent unread notifications
        recent_unread = unread_notifications[:10]
        serializer = self.get_serializer(recent_unread, many=True)
        
        return Response({
            'unread_count': unread_count,
            'notifications': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.mark_as_read()
        
        return Response({
            'message': 'Notification marked as read.',
            'notification': self.get_serializer(notification).data
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Mark a notification as unread."""
        notification = self.get_object()
        notification.mark_as_unread()
        
        return Response({
            'message': 'Notification marked as unread.',
            'notification': self.get_serializer(notification).data
        })
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        serializer = MarkAllAsReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification_ids = serializer.validated_data.get('notification_ids')
        
        if notification_ids:
            # Mark specific notifications as read
            notifications = self.get_queryset().filter(id__in=notification_ids)
        else:
            # Mark all notifications as read
            notifications = self.get_queryset().filter(read=False)
        
        updated_count = notifications.update(read=True)
        
        return Response({
            'message': f'{updated_count} notification(s) marked as read.',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['delete'])
    def delete_all_read(self, request):
        """Delete all read notifications."""
        deleted_count, _ = self.get_queryset().filter(read=True).delete()
        
        return Response({
            'message': f'{deleted_count} read notification(s) deleted.',
            'deleted_count': deleted_count
        }, status=status.HTTP_200_OK)


class NotificationStatsView(APIView):
    """View for notification statistics."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get notification statistics for the current user."""
        user = request.user
        
        total_notifications = Notification.objects.filter(recipient=user).count()
        unread_notifications = Notification.objects.filter(recipient=user, read=False).count()
        
        # Count by type
        by_type = {}
        for notification_type, _ in Notification.NOTIFICATION_TYPES:
            count = Notification.objects.filter(
                recipient=user,
                notification_type=notification_type
            ).count()
            by_type[notification_type] = count
        
        return Response({
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'notifications_by_type': by_type,
            'read_percentage': (
                ((total_notifications - unread_notifications) / total_notifications * 100)
                if total_notifications > 0 else 0
            )
        })
