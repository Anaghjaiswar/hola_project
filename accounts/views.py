from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from posts.models import Post
from posts.serializers import PostSerializer
from django.urls import reverse
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer


# Get the User model
User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Fetch the authenticated user
        serializer = UserProfileSerializer(user)  
        return Response(serializer.data)

class ShareProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Generate the shareable link
        shareable_link = request.build_absolute_uri(reverse('shared-profile', args=[request.user.id]))
        return Response({"shareable_link": shareable_link})


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Fetch the authenticated user
        serializer = UserProfileSerializer(user, data=request.data, partial=True) 

        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)  
        return Response(serializer.errors, status=400)  

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to be followed
        user_to_follow = get_object_or_404(User, id=user_id)

        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=400)

        # Add the user to the followers list
        user_to_follow.followers.add(request.user)
        return Response({"message": f"You are now following {user_to_follow.username}."})

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to be unfollowed
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if request.user == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=400)

        # Remove the user from the followers list
        user_to_unfollow.followers.remove(request.user)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}."})
    
class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        followers = user.followers.all()  # Get all followers of the user
        followers_data = [{"id": u.id, "username": u.username} for u in followers]
        return Response(followers_data)
    

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        following = user.following.all()  # Get all users the user is following
        following_data = [{"id": u.id, "username": u.username} for u in following]
        return Response(following_data)


class PublicProfileView(APIView):
    def get(self, request, user_id):
        # Get the user
        user = get_object_or_404(User, id=user_id)

        # Serialize user profile data
        user_serializer = UserProfileSerializer(user)

        # Get and serialize user's posts
        posts = Post.objects.filter(created_by=user).order_by('-created_at')
        post_serializer = PostSerializer(posts, many=True)

        return Response({
            "user_profile": user_serializer.data,
            "posts": post_serializer.data,
        })
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'full_name', 'bio']