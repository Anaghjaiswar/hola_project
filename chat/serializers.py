from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'content', 'timestamp']
