"""Models for profiles app."""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """Profile model"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='user_profile'
    )
    avatar = CloudinaryField(folder='profile_images', null=True, blank=True)
    stewardship = models.ManyToManyField(User, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """ Function to save profile data """
        super().save(*args, **kwargs)

    @property
    def avatar_url(self):
        """ Function to save users avatar """
        if self.avatar:
            return self.avatar.url
        return 'https://res.cloudinary.com/lexach91/image/upload/v1653289991/avatar_uytoij.png'
