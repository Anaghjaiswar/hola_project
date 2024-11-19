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
        user_ids = request.data.get("user_ids", [])
        users = User.objects.filter(id__in=user_ids)
        chat_room = ChatRoom.objects.create()
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
