from django.contrib import admin
from .models import Post, Comment, Like  # Add Like import


class CommentInline(admin.TabularInline):
    """Inline admin for comments."""
    
    model = Comment
    extra = 1
    readonly_fields = ['created_at', 'updated_at']


class LikeInline(admin.TabularInline):  # Add this new inline
    """Inline admin for likes."""
    
    model = Like
    extra = 1
    readonly_fields = ['created_at']
    raw_id_fields = ['user']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for posts."""
    
    list_display = ['title', 'author', 'created_at', 'like_count', 'comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'like_count', 'comment_count']
    inlines = [CommentInline, LikeInline]  



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for comments."""
    
    list_display = ['content', 'author', 'post', 'created_at']
    list_filter = ['created_at', 'author', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Like)  # Register Like model
class LikeAdmin(admin.ModelAdmin):
    """Admin interface for likes."""
    
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at', 'user', 'post']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']
