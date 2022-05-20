from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Creating profile model by extending the user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    stewardship = models.ManyToManyField(User)
    bio = models.TextField()

    def __str__(self):
        return self.user.username