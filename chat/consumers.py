import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (json to dictionary)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chat_id']
        message = await self.save_message(chat_id, username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': message.user.username,
                'chat_id': message.chat.id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_id = event['chat_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat_id': chat_id
        }))

    @database_sync_to_async      # Save message to db by converting to async
    def save_message(self, chat_id, username, message):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(username=username)
        message = Message.objects.create(chat=chat, user=user, content=message)
        return message