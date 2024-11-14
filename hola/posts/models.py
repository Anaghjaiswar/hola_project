from django.db import models
from django.contrib.auth import get_user_model

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
        return f"{self.created_by.username} - {self.content[:30]}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["created_by"]),
        ]
