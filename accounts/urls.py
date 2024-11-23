from django.urls import path
from .views import UserProfileView, EditProfileView, PublicProfileView, ShareProfileView, FollowUserView, HomepageView
from .views import FollowersListView, FollowingListView, UserListView,UserSearchView
from posts.views import UserPostsView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/<int:user_id>/posts/', UserPostsView.as_view(), name='user-posts'),
    path('profile/share/', ShareProfileView.as_view(), name='share-profile'),
    path('profile/<int:user_id>/shared/', PublicProfileView.as_view(), name='shared-profile'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='following-list'),
]
