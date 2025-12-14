from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for displaying author info."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    
    author = UserBasicSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=User.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
    
    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""
    
    author = UserBasicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 
                 'updated_at', 'like_count', 'comment_count', 'comments', 'is_liked']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 
                           'like_count', 'comment_count', 'comments']
    
    def get_is_liked(self, obj):
        """Check if the current user has liked the post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts (without nested comments)."""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        """Validate title length."""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value
    
    def validate_content(self, value):
        """Validate content length."""
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters.")
        return value


class PostUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating posts."""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        """Validate title length."""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value
    
    def validate_content(self, value):
        """Validate content length."""
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters.")
        return value
