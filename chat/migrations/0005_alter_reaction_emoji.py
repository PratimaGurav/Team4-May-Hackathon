# Generated by Django 3.2 on 2022-05-21 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='emoji',
            field=models.URLField(choices=[('thumbs_up', 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-thumbs-up_rtp2ny.gif'), ('scream', 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-scream_xkjxg7.gif'), ('cry', 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-cry_sgfigm.gif'), ('joy', 'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-joy_oxskf3.gif')]),
        ),
    ]