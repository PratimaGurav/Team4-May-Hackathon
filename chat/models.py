"""Chat app models"""
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


EMOJI_CHOICES = (
    ('https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-thumbs-up_rtp2ny.gif', 'Thumbs Up'),
    ('https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-scream_xkjxg7.gif', 'Party Scream'),
    ('https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-cry_sgfigm.gif', 'Party Cry'),
    ('https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-joy_oxskf3.gif', 'Joy'),
)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.chat_name)

    class Meta:
        """Ordering chats by created_at"""
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.chat_name, allow_unicode=True)
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Message model"""
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    content = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField(
        'chat_image',
        folder='chat_images',
        null=True,
        blank=True
    )

    def __str__(self): 
        return str(self.id)

    class Meta:
        """ Order messages by creation date. """
        ordering = ['created_at']

    @property
    def get_reactions_with_users(self):
        reactions = self.reactions.all()
        # every reaction has a user and emoji url
        # we need to find the count of each emoji url
        # see what users have reacted to this message
        # and count the number of times each emoji url is used
        # {'emoji_url': [user1, user2, user3], 'emoji_url': [user1, user2, user3]}
        reactions_with_users = {}
        for reaction in reactions:
            if reaction.emoji in reactions_with_users:
                reactions_with_users[reaction.emoji].append(reaction.user.username)
            else:
                reactions_with_users[reaction.emoji] = [reaction.user.username]
        return reactions_with_users
        
        

class Reaction(models.Model):
    """Reaction model"""
    chat_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    emoji = models.URLField()    
        
    def __str__(self):
        return f'{self.user.username} reacted with {self.emoji}'
