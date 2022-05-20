import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Chat, ChatMessage
# need to import base64
import base64
from django.core.files.base import ContentFile
from django.core.files import File
import cloudinary
import cloudinary.uploader


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
        # print(text_data)
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chat_id']
        image = text_data_json['image']
        # image is data:image/png;base64 or data:image/jpeg;base64 that needs to be read as a file and passed to the CloudinaryField of the ChatMessage model
        
        if image:
            image_data = image.split(',')[1]
            image_extension = image.split(';')[0].split('/')[1]
            image_name = f'{username}_{chat_id}_{random.randint(1, 100)}.{image_extension}'
            image_file = ContentFile(base64.b64decode(image_data), name=image_name)
            image_file = File(image_file)
        else:
            image_file = None
        
        
        
        message = await self.save_message(chat_id, username, message, image_file)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': message.user.username if message.user else None,
                'chat_id': message.chat.id,
                'image': message.image if message.image else None,
                # time format May 20, 2022, 7:55 a.m.
                'time': message.created_at.strftime("%b %d, %Y, %I:%M %p")
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_id = event['chat_id']
        image = event['image']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat_id': chat_id,
            'image': image,
            'time': time
        }))

    @database_sync_to_async      # Save message to db by converting to async
    def save_message(self, chat_id, username, message, image_file):
        chat = Chat.objects.get(id=chat_id)
        if username == 'Anonymous':
            user = None
        else:
            user = User.objects.get(username=username)
        
        # upload image to cloudinary and save it to the image CloudinaryField of the ChatMessage model
        if image_file:
            image = cloudinary.uploader.upload(image_file, folder='chat_images')
            image = image['url']
            message = ChatMessage.objects.create(chat=chat, content=message, image=image)        
        else:
            message = ChatMessage.objects.create(chat=chat, content=message)
        
        if user:
            message.user = user
        message.save()
        
        return message
    