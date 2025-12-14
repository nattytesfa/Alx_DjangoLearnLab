from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator


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
    content = models.TextField(
        validators=[MinLengthValidator(10, "Content must be at least 10 characters.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )
    
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
    content = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(2, "Comment must be at least 2 characters.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
