# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from django.contrib.auth import get_user_model


User = get_user_model()

class GetOrCreateConversation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_user_id = request.data.get('target_user_id')

        if not target_user_id:
            return Response({"error": "Target user ID is required"}, status=400)

        try:
            target_user = User.objects.get(id=target_user_id)
        except User.DoesNotExist:
            return Response({"error": "Target user not found"}, status=404)

        # Ensure users aren't creating conversations with themselves
        if target_user == request.user:
            return Response({"error": "Cannot create a conversation with yourself"}, status=400)

        # Check if a conversation already exists
        conversation = Conversation.objects.filter(
            user1=request.user, user2=target_user
        ).first() or Conversation.objects.filter(
            user1=target_user, user2=request.user
        ).first()

        if not conversation:
            # Create a new conversation
            conversation = Conversation.objects.create(user1=request.user, user2=target_user)

        return Response({
            "conversation_id": conversation.id,
            "message": "Conversation fetched or created successfully"
        })
    

class UnreadCountView(APIView):
    def get(self, request):
        user = request.user
        unread_count = Message.objects.filter(recipient=user, status='unread').count()
        return Response({'unread_count': unread_count})
