from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    actor_profile_picture = serializers.SerializerMethodField()
    target_object = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'actor_username', 'actor_profile_picture',
            'verb', 'notification_type', 'target', 'target_object',
            'read', 'timestamp', 'time_since'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_actor_profile_picture(self, obj):
        """Get actor's profile picture URL."""
        if obj.actor.profile_picture:
            return obj.actor.profile_picture.url
        return None
    
    def get_target_object(self, obj):
        """Get serialized target object if it exists."""
        if obj.target:
            # You can customize this based on your target models
            if hasattr(obj.target, 'title'):  # For posts
                return {'id': obj.target.id, 'title': obj.target.title}
            elif hasattr(obj.target, 'content'):  # For comments
                return {'id': obj.target.id, 'content': obj.target.content[:50] + '...'}
        return None
    
    def get_time_since(self, obj):
        """Get human-readable time since notification was created."""
        from django.utils import timezone
        from django.utils.timesince import timesince
        
        return timesince(obj.timestamp, timezone.now()) + ' ago'


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notifications (mark as read/unread)."""
    
    class Meta:
        model = Notification
        fields = ['read']


class MarkAllAsReadSerializer(serializers.Serializer):
    """Serializer for marking all notifications as read."""
    
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
