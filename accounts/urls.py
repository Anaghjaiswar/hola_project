from django.urls import path
from .views import UserProfileView, EditProfileView, PublicProfileView, ShareProfileView
from .views import FollowUserView, UnfollowUserView, FollowersListView, FollowingListView
from posts.views import PostListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/<int:user_id>/posts/', PostListView.as_view(), name='user-posts'),
     path('profile/share/', ShareProfileView.as_view(), name='share-profile'),
    path('profile/<int:user_id>/shared/', PublicProfileView.as_view(), name='shared-profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='following-list'),
]
