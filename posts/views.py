from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like, Comment, CommentLike
from rest_framework.generics import ListCreateAPIView
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from django.db.models import F
from accounts.models import CustomUser

# Create a new post
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific post
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.created_by != request.user:
            return Response({"error": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.created_by != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)

# List all posts
class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(is_public=True).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    

class UserPostsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        posts = Post.objects.filter(created_by=user).order_by('-created_at') 
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if the user already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a like instance
        Like.objects.create(user=request.user, post=post)
        
        # Increment the likes count
        post.likes_count = F('likes_count') + 1
        post.save()

        return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)
    

class UnlikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        # Decrement the likes count
        post.likes_count = F('likes_count') - 1
        post.save()

        return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id, parent_comment=None).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        parent_comment_id = self.request.data.get('parent_comment')
        parent_comment = Comment.objects.filter(id=parent_comment_id).first()
        
        comment = serializer.save(user=self.request.user, post=post, parent_comment=parent_comment)
        
        # Increment comments count for the post
        post.comments_count = F('comments_count') + 1
        post.save()
        
        return comment
    
class LikeUnlikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user already liked the comment
        if CommentLike.objects.filter(user=request.user, comment=comment).exists():
            return Response({"detail": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a like instance
        CommentLike.objects.create(user=request.user, comment=comment)

        # Increment the likes count
        comment.likes_count = F('likes_count') + 1
        comment.save()

        return Response({"detail": "Comment liked successfully!"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = CommentLike.objects.filter(user=request.user, comment=comment).first()

        if not like:
            return Response({"detail": "You have not liked this comment."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        # Decrement the likes count
        comment.likes_count = F('likes_count') - 1
        comment.save()

        return Response({"detail": "Comment unliked successfully!"}, status=status.HTTP_200_OK)

class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        post_author = comment.post.created_by

        # print("Request user:", request.user)
        # print("Comment user:", comment.user)
        # print("Post author:", Post.created_by)
    

        # Check if the logged-in user is the author of the comment
        if comment.user != request.user  and request.user != post_author:
            return Response(
                {"error": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Delete the comment
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully."},
            status=status.HTTP_200_OK
        )