# Generated by Django 3.2 on 2022-05-21 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_alter_chatmessage_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.IntegerField(choices=[(1, 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-thumbs-up_rtp2ny.gif'), (2, 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-scream_xkjxg7.gif'), (3, 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-cry_sgfigm.gif'), (4, 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-joy_oxskf3.gif')])),
                ('chat_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='chat.chatmessage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
