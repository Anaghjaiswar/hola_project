from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Get the user model once, outside the class
User = get_user_model()

# Model for a Chat Room
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)  # Name of the chat room
    participants = models.ManyToManyField(User, related_name='chatrooms')  # Participants in the chat room
    created_by = models.ForeignKey(User, related_name='created_chatrooms', on_delete=models.CASCADE)  # Creator of the chat room
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Message from {self.sender.get_full_name()} in Room {self.chat_room.id}"

# Model for a Chat Message
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} in {self.room_name}: {self.content}'
