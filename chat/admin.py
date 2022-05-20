from django.contrib import admin
from .models import Chat, ChatMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'chat_description', 'slug')
    prepopulated_fields = {'slug': ('chat_name',)}
    search_fields = ('chat_name',)
    ordering = ['chat_name']
    
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'content', 'created_at', 'image')
    list_filter = ('chat', 'user', 'created_at')
    search_fields = ('content',)
    ordering = ['-created_at']