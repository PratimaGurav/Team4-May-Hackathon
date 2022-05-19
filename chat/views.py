from django.shortcuts import render
from django.views import View


class chatView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chat/chat.html', {
            'chat_room': 'helloAlex'
        })