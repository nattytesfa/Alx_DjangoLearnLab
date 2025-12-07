from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """
    Blog Post model representing a blog post/article.
    
    Fields:
    - title: CharField with max length of 200 characters
    - content: TextField for the main content of the post
    - published_date: DateTimeField automatically set when post is created
    - author: ForeignKey linking to Django's User model
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Delete posts if user is deleted
        related_name='posts'  # Enables user.posts.all() to get all posts by user
    )
    
    def __str__(self):
        """
        String representation of the Post model.
        """
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        """
        Returns the URL to access a detail view of this post.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        """
        Metadata for the Post model.
        """
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_date']  # Show newest posts first


class Comment(models.Model):
    """
    Comment model for blog post comments.
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
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        ordering = ['-created_date']


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
