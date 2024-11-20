from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Fetch the authenticated user
        serializer = UserProfileSerializer(user)  # Serialize the user's profile data
        return Response(serializer.data)

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Fetch the authenticated user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)  # Serialize and validate the data

        if serializer.is_valid():
            serializer.save()  # Save the updated profile data
            return Response(serializer.data)  # Return the updated data
        return Response(serializer.errors, status=400)  # Return validation errors if any
