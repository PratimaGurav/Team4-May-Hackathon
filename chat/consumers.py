import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Chat, ChatMessage, Reaction
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
        text_data_json = json.loads(text_data)
        
        message_type = text_data_json['type']
        if message_type == 'chat_message':
            message = text_data_json['message']
            username = text_data_json['username']
            chat_id = text_data_json['chat_id']
            image = text_data_json['image']
            
            if image:
                image_data = image.split(',')[1]
                image_extension = image.split(';')[0].split('/')[1]
                image_name = f'{username}_{chat_id}_{random.randint(1, 100)}.{image_extension}'
                image_file = ContentFile(base64.b64decode(image_data), name=image_name)
                image_file = File(image_file)
            else:
                image_file = None
            
            
            
            message = await self.save_message(chat_id, username, message, image_file)
            avatar_url = await self.get_avatar_url(username)

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
                    'time': message.created_at.strftime("%b %d, %Y, %I:%M %p"),
                    'message_id': message.id,
                    'avatar_url': avatar_url
                }
            )
        elif message_type == 'message_reaction':
            username = text_data_json['username']
            message_id = text_data_json['message_id']
            emoji_url = text_data_json['emoji_url']
            
            await self.add_remove_reaction(message_id, username, emoji_url)
            reactions = await self.get_reactions(message_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_reaction',
                    'reactions': reactions,
                    'message_id': message_id
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_id = event['chat_id']
        image = event['image']
        time = event['time']
        message_id = event['message_id']
        avatar_url = event['avatar_url']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
            'chat_id': chat_id,
            'image': image,
            'time': time,
            'message_id': message_id,
            'avatar_url': avatar_url
        }))
        
    async def message_reaction(self, event):
        reactions = event['reactions']
        message_id = event['message_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message_reaction',
            'reactions': reactions,
            'message_id': message_id
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
    
    @database_sync_to_async
    def add_remove_reaction(self, chat_message_id, username, emoji):
        chat_message = ChatMessage.objects.get(id=chat_message_id)
        user = User.objects.get(username=username)
        reaction = Reaction.objects.filter(chat_message=chat_message, user=user, emoji=emoji)
        if reaction:
            reaction[0].delete()            
        else:
            reaction = Reaction.objects.create(chat_message=chat_message, user=user, emoji=emoji)
            reaction.save()
    
    @database_sync_to_async
    def get_reactions(self, chat_message_id):
        chat_message = ChatMessage.objects.get(id=chat_message_id)
        return chat_message.get_reactions_with_users
    
    @database_sync_to_async
    def get_avatar_url(self, username):
        if username == 'Anonymous':
            return 'https://res.cloudinary.com/lexach91/image/upload/v1653289991/avatar_uytoij.png'
        return User.objects.get(username=username).user_profile.avatar_url