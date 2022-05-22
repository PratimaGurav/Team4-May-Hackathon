"""Forms for the profiles app."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """ Class for User Registration Form """
    email = forms.EmailField()

    class Meta:
        """ Class setting user registration fields """
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    """ Class for Update User Form """
    email = forms.EmailField()

    class Meta:
        """ Class for Update User fields """
        model = User
        fields = ['username', 'email']


# Create a ProfileUpdateForm to update profile image
class ProfileUpdateForm(forms.ModelForm):
    """ Class for updating user profiles """
    class Meta:
        """ Class for fields updating user profiles """
        model = Profile
        fields = ['avatar', 'bio']
