"""
Django settings for apps.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""


from django.apps import AppConfig
from django.db.models.signals import post_save


class ProfilesConfig(AppConfig):
    """ Class to configure apps settings """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        """ Function to configure apps settings """
        from profiles.signals import create_profile
        from django.contrib.auth.models import User
        post_save.connect(create_profile, sender=User)
        from profiles.signals import save_profile
        post_save.connect(save_profile, sender=User)
