from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    """Inline admin for comments."""
    
    model = Comment
    extra = 1
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for posts."""
    
    list_display = ['title', 'author', 'created_at', 'like_count', 'comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'like_count', 'comment_count']
    inlines = [CommentInline]
    filter_horizontal = ['likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for comments."""
    
    list_display = ['content', 'author', 'post', 'created_at']
    list_filter = ['created_at', 'author', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
