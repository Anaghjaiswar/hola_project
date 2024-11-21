from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateChatRoomView(APIView):
    def post(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        user_ids = request.data.get("user_ids", [])
        users = User.objects.filter(id__in=user_ids)

        # Create a chat room and set the creator
        chat_room = ChatRoom.objects.create(created_by=request.user)
        chat_room.participants.set(users)
        chat_room.save()

        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListView(APIView):
    def get(self, request, chat_room_id):
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        messages = chat_room.messages.all().order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
