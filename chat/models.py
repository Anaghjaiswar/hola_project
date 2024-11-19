from django.db import models
from django.contrib.auth import get_user_model

# Get the user model once, outside the class
User = get_user_model()

# Model for a Chat Room
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)  # Name of the chat room
    participants = models.ManyToManyField(User, related_name='chatrooms')  # Participants in the chat room
    created_by = models.ForeignKey(User, related_name='created_chatrooms', on_delete=models.CASCADE)  # Creator of the chat room
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Model for a Chat Message
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender}"
