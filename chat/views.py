from django.shortcuts import render
from django.views import View
from .models import Chat, Message


class ChatRoomView(View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.get(slug=kwargs['slug'])
        messages = Message.objects.filter(chat=chat).order_by('-created_at')
        return render(
            request,
            'chat/chat_room.html',
            {
                'chat': chat,     
            }
        )


class ChatListView(View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.all()
        return render(
            request,
            'chat/chat_list.html',
            {'chats': chats}
        )