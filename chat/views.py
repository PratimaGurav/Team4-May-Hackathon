"""Views for the chat app."""
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Chat, ChatMessage, Reaction


EMOJI_LIST = [
    'https://res.cloudinary.com/lexach91/image/upload/v1653219641/emojis/party-scream_r5mkrv.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219640/emojis/giphy-strong_xhwx9e.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219640/emojis/giphy-rofl_em7zvl.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219641/emojis/party-heart-slow_dnjbzs.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219641/emojis/giphy-tired_r5fdgh.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219641/emojis/party-cry_mdly2m.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219640/emojis/giphy-smirk_n7hkjq.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219640/emojis/giphy-thumbs-up_bioc3a.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-pray_okjluh.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219640/emojis/giphy-scream_or8ait.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-raised-hands_xcm879.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-poop_dim7xj.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219637/emojis/giphy-grin_k88yg4.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-peace_pz3lr8.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-pensive_kmwtjc.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219639/emojis/giphy-okay_jzcptr.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219638/emojis/giphy-laughing_fm6ooa.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219638/emojis/giphy-kiss_wq6eyk.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219638/emojis/giphy-joy_btlfsy.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219638/emojis/giphy-hug_pfzrk9.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219637/emojis/giphy-hearts_n3vwba.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219637/emojis/giphy-deflate_tfqjhj.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219637/emojis/giphy-eye-roll_no35gn.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-exploding_j0a7v2.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-cool_yczev2.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-confused_yzohyu.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-confetti_hjsolp.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-cry_qf3dy0.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219636/emojis/giphy-chefs-kiss_idzzns.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219635/emojis/could-you-not_cgagli.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219634/emojis/giphy-100_jtljgu.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219634/emojis/deal-with-it-parrot_rg3h7p.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219634/emojis/blob-happy_hgjd8m.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219634/emojis/dance-banana_cxfkvr.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653219633/emojis/cat-confused_ayscim.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653110064/emojis/giphy-blush-masked_er8ibb.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653110063/emojis/giphy-beers_hbow7k.gif',
]

class ChatRoomView(View):
    """ChatRoomView"""
    def get(self, request, *args, **kwargs):
        # if user is authenticated
        if request.user.is_authenticated:
            chat = Chat.objects.get(slug=kwargs['slug'])

            chats = Chat.objects.all()

            return render(
                request,
                'chat/chat_room.html',
                {
                    'chat': chat,
                    'chats': chats,
                    'emojis': EMOJI_LIST
                }
            )


class ChatListView(View):
    """ChatListView"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            chats = Chat.objects.all()
            return render(
                request,
                'chat/chat_list.html',
                {'chats': chats}
            )
