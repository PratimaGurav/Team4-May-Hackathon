"""Views for the chat app."""
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Chat, ChatMessage, Reaction


EMOJI_LIST = [
        'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-thumbs-up_rtp2ny.gif',
        'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-scream_xkjxg7.gif',
        'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-cry_sgfigm.gif',
        'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-joy_oxskf3.gif'
]

class ChatRoomView(View):
    """ChatRoomView"""
    def get(self, request, *args, **kwargs):
        # if user is authenticated
        if request.user.is_authenticated:
            chat = Chat.objects.get(slug=kwargs['slug'])

            chats = Chat.objects.all()

            return render(
                request,
                'chat/chat_room.html',
                {
                    'chat': chat,
                    'chats': chats,
                    'emojis': EMOJI_LIST
                }
            )


class ChatListView(View):
    """ChatListView"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            chats = Chat.objects.all()
            return render(
                request,
                'chat/chat_list.html',
                {'chats': chats}
            )
