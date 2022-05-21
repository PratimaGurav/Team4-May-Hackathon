from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Chat(models.Model):
    """Chat model"""
    chat_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True)
    chat_description = models.CharField(max_length=250)
    chat_logo = CloudinaryField(
        'chat_logo',
        folder='chat_logo',
        null=True,
        blank=True
    )
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_name

    class Meta:
        """Ordering chats by created_at"""
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.chat_name, allow_unicode=True)
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Message model"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField(
        'chat_image',
        folder='chat_images',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.content

    class Meta:
        """ Order messages by creation date. """
        ordering = ['created_at']
