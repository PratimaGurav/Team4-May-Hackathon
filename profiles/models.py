"""Models for profiles app."""
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Profile(models.Model):
    """Profile model"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='user_profile'
    )
    avatar = CloudinaryField(folder='profile_images')
    stewardship = models.ManyToManyField(User, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
    
    @property    
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/media/profile_images/avatar.png'
