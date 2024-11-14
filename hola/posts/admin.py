from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'content', 'is_public', 'created_at')
    search_fields = ('content', 'created_by__username')
    list_filter = ('is_public', 'created_at')
