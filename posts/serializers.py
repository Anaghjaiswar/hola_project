from rest_framework import serializers
from .models import Post, Like, Comment, CommentLike

class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.full_name', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    profile_photo = serializers.ImageField(source='created_by.profile_photo', required=False)
    media = serializers.FileField()


    class Meta:
        model = Post
        fields = ['id', 'created_by', 'content', 'media', 'created_at', 'updated_at', 'is_public', 'likes_count', 'comments_count', 'tags','profile_photo']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'likes_count', 'comments_count']

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Content cannot be empty.")
        return value
    


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes = CommentLikeSerializer(many=True, read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'parent_comment', 'likes_count', 'created_at', 'updated_at', 'likes', 'replies']
        read_only_fields = ['user', 'post', 'likes_count', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []