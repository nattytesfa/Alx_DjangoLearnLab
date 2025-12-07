from django.contrib import admin
from .models import Post, Comment, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'short_content')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'published_date'
    
    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    short_content.short_description = 'Content Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_preview')
    search_fields = ('name', 'description')
    
    def description_preview(self, obj):
        return obj.description[:100] + '...' if obj.description else 'No description'
    description_preview.short_description = 'Description'
