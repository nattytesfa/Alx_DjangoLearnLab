from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for notifications."""
    
    list_display = ['id', 'recipient', 'actor', 'verb', 'notification_type', 'read', 'created_at']
    list_filter = ['notification_type', 'read', 'created_at']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['created_at']
    list_per_page = 20
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.update(read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    
    mark_as_read.short_description = "Mark selected notifications as read"
    mark_as_unread.short_description = "Mark selected notifications as unread"
