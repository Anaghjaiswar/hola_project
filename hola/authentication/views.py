from rest_framework.views import APIView
from social_django.utils import psa
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.db.utils import IntegrityError

User = get_user_model()

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save the user if valid
                serializer.save()
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

            except IntegrityError:
                # Handle duplicate email registration
                return Response({"message": "User with this email is already registered."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GoogleLogin(APIView):
    def get(self, request, *args, **kwargs):
        # The URL for Google OAuth login
        return Response({"message": "Redirecting to Google for authentication."}, status=status.HTTP_200_OK)

class GoogleCallback(APIView):
    @psa('social:complete')
    def get(self, request, *args, **kwargs):
        # Handle the callback from Google after user authentication
        user = request.user
        if user.is_authenticated:
            # Perform your user login or registration logic
            return Response({"message": f"Welcome {user.full_name}!"}, status=status.HTTP_200_OK)
        return Response({"message": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)
