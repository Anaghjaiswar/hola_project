from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='conversation_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='conversation_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.user1.get_full_name()} and {self.user2.get_full_name()}"

    def participants(self):
        """Returns a list of participants in the conversation."""
        return [self.user1.get_full_name(), self.user2.get_full_name()]

    class Meta:
        unique_together = ('user1', 'user2')  # Ensure only one conversation between two users
        ordering = ['-created_at']


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('read', 'Read')], default='sent')

    def __str__(self):
        return f"Message from {self.sender.get_full_name()} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']  # Sort by timestamp


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, related_name='statuses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='message_statuses', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('unread', 'Unread'), ('read', 'Read')], default='unread')

    def __str__(self):
        return f"Status of {self.message} for {self.user.get_full_name()}"

    class Meta:
        unique_together = ('message', 'user')  


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.get_full_name()} about message {self.message}"

    class Meta:
        ordering = ['-created_at']  