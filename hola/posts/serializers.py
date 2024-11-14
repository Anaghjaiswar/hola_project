from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'created_by', 'content', 'media', 'created_at', 'updated_at', 'is_public', 'likes_count', 'comments_count', 'tags']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'likes_count', 'comments_count']

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Content cannot be empty.")
        return value
