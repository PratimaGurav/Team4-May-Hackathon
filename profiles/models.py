from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


# Creating profile model by extending the user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avatar = CloudinaryField(folder='profile_images')
    stewardship = models.ManyToManyField(User, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/media/profile_images/avatar.png'


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.user_profile.save()