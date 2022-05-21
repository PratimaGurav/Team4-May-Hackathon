from django.shortcuts import render
from django.contrib import messages
from django.views import View
from chat.models import Chat


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.all()
        return render(request, 'index.html', {'chat': chat})

class ContactView(View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.all()
        return render(request, 'contact-us.html', {})