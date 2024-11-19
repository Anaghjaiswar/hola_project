from django.urls import path
from .views import PostCreateView, PostDetailView, PostListView, LikePostAPIView, UnlikePostAPIView, CommentListCreateAPIView,LikeUnlikeCommentAPIView, CommentDeleteAPIView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('<int:post_id>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
    path('<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comments-list-create'),
    path('comments/<int:comment_id>/like/', LikeUnlikeCommentAPIView.as_view(), name='like-comment'),
    path('comments/<int:comment_id>/unlike/', LikeUnlikeCommentAPIView.as_view(), name='unlike-comment'),
    path('comments/<int:comment_id>/delete/', CommentDeleteAPIView.as_view(), name='delete-comment'),
]