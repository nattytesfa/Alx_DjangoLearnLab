from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    """Model representing a like on a post."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # Prevent duplicate likes
        ordering = ['-created_at']
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
    
    def save(self, *args, **kwargs):
        """Override save to send notification."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Send notification for new like
        if is_new:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=self.post.author,
                actor=self.user,
                verb='liked your post',
                target=self.post
            )


class Post(models.Model):
    """Model representing a blog post."""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5, "Title must be at least 5 characters.")]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Replace ManyToManyField with GenericRelation to Like
    likes = GenericRelation(Like, related_query_name='post')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f'{self.title} by {self.author.username}'
    
    @property
    def like_count(self):
        """Return the number of likes on the post."""
        return self.likes.count()
    
    @property
    def comment_count(self):
        """Return the number of comments on the post."""
        return self.comments.count()
    
    def user_has_liked(self, user):
        """Check if a specific user has liked this post."""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class Comment(models.Model):
    """Model representing a comment on a post."""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def save(self, *args, **kwargs):
        """Override save to send notification."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Send notification for new comment (except when author comments on own post)
        if is_new and self.author != self.post.author:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=self.post.author,
                actor=self.author,
                verb='commented on your post',
                target=self.post
            )
