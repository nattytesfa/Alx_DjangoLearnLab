from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    """
    Blog Post model representing a blog post/article.
    """
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_comment_count(self):
        """Get the number of approved comments."""
        return self.comments.filter(approved=True).count()
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Comment model for blog post comments with enhanced features.
    
    Fields:
    - post: ForeignKey to the Post model
    - author: ForeignKey to the User model
    - content: TextField for comment text
    - created_at: DateTimeField for creation timestamp
    - updated_at: DateTimeField for update timestamp
    - approved: BooleanField for comment approval status
    - parent: ForeignKey to self for nested replies (optional)
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def is_edited(self):
        """Check if comment has been edited."""
        return self.updated_at > self.created_at
    
    def get_absolute_url(self):
        """Get URL to view this comment."""
        return reverse('post-detail', kwargs={'pk': self.post.pk}) + f'#comment-{self.pk}'
    
    def can_edit(self, user):
        """Check if user can edit this comment."""
        return user == self.author or user.is_superuser
    
    def can_delete(self, user):
        """Check if user can delete this comment."""
        return user == self.author or user.is_superuser or user == self.post.author
    
    def get_reply_count(self):
        """Get number of replies to this comment."""
        return self.replies.count()
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Category(models.Model):
    """
    Category model for organizing blog posts.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
