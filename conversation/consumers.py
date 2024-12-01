import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Check if the user is authenticated
        # if not self.scope['user'].is_authenticated:
        #     await self.close()
        #     return

        # Join the conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the incoming message
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if not message:  # Reject empty messages
                return

            sender = self.scope['user']
            conversation = await self.get_conversation(self.conversation_id)

            if not conversation:
                await self.send(json.dumps({'error': 'Invalid conversation ID'}))
                return

            # Save and broadcast the message
            new_message = await self.create_message(conversation, sender, message)
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'chat_message',
                    'message': new_message.text,
                    'sender': sender.email,
                    'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
        except json.JSONDecodeError:
            await self.send(json.dumps({'error': 'Invalid message format'}))


    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.select_related('user1', 'user2').get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, sender, message):
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=message
        )