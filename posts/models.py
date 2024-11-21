from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

User = get_user_model()

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    media = models.FileField(upload_to="posts/media/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.created_by.get_full_name} - {self.content[:30]}"
    
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["created_by"]),
        ]


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} liked {self.post.content[:30]}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

    class Meta:
        ordering = ['created_at']


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"