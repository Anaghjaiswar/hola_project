from django.urls import path
from .views import GetOrCreateConversation


urlpatterns = [
    path('', GetOrCreateConversation.as_view(), name='conversation-id'),
]
