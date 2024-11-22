from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageAPIView

urlpatterns = [
    path('messages/',MessageAPIView.as_view())
]