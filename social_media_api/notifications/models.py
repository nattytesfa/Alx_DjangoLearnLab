from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    """Model representing a user notification."""
    
    NOTIFICATION_TYPES = [
        ('follow', 'New Follower'),
        ('like', 'Post Like'),
        ('comment', 'Post Comment'),
        ('mention', 'Mention'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_sent'
    )
    verb = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system'
    )
    
    # Generic foreign key for the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', 'read', 'created_at']),
            models.Index(fields=['recipient', 'notification_type']),
        ]
    
    def __str__(self):
        return f'{self.actor.username} {self.verb}'
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.read = True
        self.save()
    
    def mark_as_unread(self):
        """Mark notification as unread."""
        self.read = False
        self.save()
    
    @classmethod
    def create_follow_notification(cls, recipient, actor):
        """Create a notification for a new follower."""
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='started following you',
            notification_type='follow'
        )
    
    @classmethod
    def create_like_notification(cls, recipient, actor, post):
        """Create a notification for a post like."""
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='liked your post',
            notification_type='like',
            target=post
        )
    
    @classmethod
    def create_comment_notification(cls, recipient, actor, post):
        """Create a notification for a post comment."""
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='commented on your post',
            notification_type='comment',
            target=post
        )
