from django.urls import path
from .views import RegisterUserView, GoogleCallback
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('complete/google/', GoogleCallback.as_view(), name='google_callback'),  # Callback after successful login
]
