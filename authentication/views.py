from rest_framework.views import APIView
from social_django.utils import psa
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.db.utils import IntegrityError
from django.contrib.auth import login
from requests.exceptions import HTTPError
from .serializers import ChangePasswordSerializer
from .models import PasswordResetOTP
from django.core.mail import send_mail
from datetime import timedelta

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
        # Extract authorization code from request
        code = request.GET.get('code')
        if not code:
            return Response({"message": "Authorization code not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Using python-social-auth to complete the login process
            user = request.backend.do_auth(code)
            if user and user.is_authenticated:
                login(request, user)
                return Response({"message": f"Welcome {user.full_name}!"}, status=status.HTTP_200_OK)
            return Response({"message": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)

        except HTTPError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ForgotPasswordView(APIView):
    """
    Request OTP for password reset.
    """
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        otp = PasswordResetOTP.objects.create(
            user=user,
            otp=PasswordResetOTP().generate_otp(),
            expired_at=timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        )
        
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp.otp}',
            'jaiswaranagh@gmail.com',  
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """
    Verify OTP and reset password.
    """
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            reset_otp = PasswordResetOTP.objects.get(user=user, otp=otp)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if OTP is expired
        if reset_otp.is_expired():
            return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Reset password
        user.set_password(new_password)
        user.save()

        # Optionally, delete the OTP record after use
        reset_otp.delete()

        return Response({"message": "Password successfully reset."}, status=status.HTTP_200_OK)


























from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
@login_required
def test_redirect_view(request):
    return HttpResponse(f"Welcome, {request.user.email}! You are logged in.")