from django.urls import path
from .views import UserProfileView, EditProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
]
