/* jshint esversion: 6, jquery: true */
document.addEventListener('DOMContentLoaded', function () {
  const roomName = window.location.pathname.split('/')[2];
  const chatContainer = document.getElementsByClassName('chat__container')[0];
  const chatInput = document.getElementById('chat-input');
  const fileInput = document.getElementById('chat-file');
  const sendButton = document.getElementById('chat-send');
  const sendAnonymouslyCheckbox = document.getElementById('send-anonymously');
  const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const socketUrl = `${socketProtocol}//${window.location.host}/ws/chat/${roomName}/`;
  const chatSocket = new WebSocket(socketUrl);

  const navbarItems = document.getElementsByClassName('chats__navbar--item');
  for (let i = 0; i < navbarItems.length; i++) {
    if (navbarItems[i].href === window.location.href) {
      navbarItems[i].classList.add('chats__navbar--item--active');
    }
  }

  const reactionsTogglers = $('.reactions__toggle');
  const reactionsChoicesContainers = $('.reactions__choices');
  const emojiLinks = [
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
  ];

  // initialize emojiOneArea on chatInput
  $('#chat-input').emojioneArea({
    useSprite: true,
  });


  const hideReactions = () => {
    $('.reactions__choices').addClass('hidden');
  };

  $('.reactions__toggle').click(function (e) {
    e.stopPropagation();
    $('.reactions__choices').addClass('hidden');
    // find sibling with class reactions__choices and toggle class hidden
    // then add class hidden if clicked outside of it
    const reactionsChoicesContainer = $(this).siblings('.reactions__choices');
    if (reactionsChoicesContainer.hasClass('hidden')) {
      reactionsChoicesContainer.removeClass('hidden');
    } else {
      reactionsChoicesContainer.addClass('hidden');
    }
    $(document).click(function (e) {
      // if clicked outside of reactions__choices and not on reactions__toggle then hide reactions
      if (!$('.reactions__toggle').is(e.target) && reactionsChoicesContainer.has(e.target).length === 0) {
        hideReactions();
        // remove event listener
        $(document).off('click');
      }
    });
  });

  const chatId = document.getElementById('chat-id').value;
  const username = document.getElementById('username').value;


  // scroll to bottom of chat
  chatContainer.scrollTop = chatContainer.scrollHeight + 100;

  chatSocket.onopen = function () {
    console.log('Connected to chat server');
  };

  chatSocket.onclose = function () {
    console.log('Disconnected from chat server');
  };

  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    if (data.type === 'chat_message') {

      let message = document.createElement('div');
      message.classList.add('message');
      message.setAttribute('data-message-id', data.message_id);
      let messageHeader = document.createElement('div');
      messageHeader.classList.add('message__header');
      let messageHeaderData = document.createElement('div');
      messageHeaderData.classList.add('message__header--data');
      let messageHeaderAvatar = document.createElement('div');
      messageHeaderAvatar.classList.add('message__avatar--avatar');
      let messageHeaderUsername = document.createElement('div');
      messageHeaderUsername.classList.add('message__header--username');
      let messageHeaderTime = document.createElement('div');
      messageHeaderTime.classList.add('message__header--time');
      let messageBody = document.createElement('div');
      messageBody.classList.add('message__body');
      let messageBodyText = document.createElement('div');
      messageBodyText.classList.add('message__body--text');
      let messageBodyImage = document.createElement('div');
      messageBodyImage.classList.add('message__body--image');
      // messageHeaderUsername.innerHTML = data.username || 'Anonymous';
      messageHeaderUsername.innerHTML = data.username ? `<a class="message__header--username message__header--link" href="/profile/${data.username}/">${data.username}</a>` : 'Anonymous';
      messageHeaderTime.innerHTML = data.time;
      messageBodyText.innerHTML = data.message;
      if (data.image) {
        messageBodyImage.innerHTML = `<img src="${data.image}" />`;
      }
      messageHeaderAvatar.innerHTML = `<img src="${data.avatar_url}" alt="Avatar of ${data.username ? data.username : 'Anonymous'}" />`;
      messageHeader.appendChild(messageHeaderData);
      messageHeaderData.appendChild(messageHeaderAvatar);
      messageHeaderData.appendChild(messageHeaderUsername);
      messageHeaderData.appendChild(messageHeaderTime);
      message.appendChild(messageHeader);
      message.appendChild(messageBody);
      messageBody.appendChild(messageBodyText);
      if (data.image) {
        messageBody.appendChild(messageBodyImage);
      }
      let messageReactions = document.createElement('div');
      messageReactions.classList.add('message__reactions');
      let messageReactionsContainer = document.createElement('div');
      messageReactionsContainer.classList.add('message__reactions--container');
      // add data-message-id to messageReactionsContainer
      messageReactionsContainer.setAttribute('data-message-id', data.message_id);
      let messageReactionsChoices = document.createElement('div');
      messageReactionsChoices.classList.add('message__reactions--choices');
      // add reaction button to messageReactionsChoices
      let reactionsToggle = document.createElement('span');
      reactionsToggle.classList.add('reactions__toggle');
      reactionsToggle.innerHTML = `
      <i class="far fa-grin"></i>
      <div class="reactions__toggle--plus">+</div>
      `;
      reactionsToggle.addEventListener('click', function (e) {
        $(this).siblings('.reactions__choices').toggleClass('hidden');
      });
      let reactionsChoices = document.createElement('div');
      reactionsChoices.classList.add('reactions__choices');
      reactionsChoices.classList.add('hidden');
      for (let emoji_url of emojiLinks) {
        let reaction = document.createElement('div');
        let reactionImg = document.createElement('img');
        reactionImg.setAttribute('src', emoji_url);
        reactionImg.setAttribute('data-message-id', data.message_id);
        reactionImg.classList.add('reaction_emoji--img');
        reaction.appendChild(reactionImg);
        reactionsChoices.appendChild(reaction);
        // add event listener to reaction
        reactionImg.addEventListener('click', reactionHandler);
      }
      messageReactions.appendChild(messageReactionsContainer);
      messageReactions.appendChild(messageReactionsChoices);
      messageReactionsChoices.appendChild(reactionsToggle);
      messageReactionsChoices.appendChild(reactionsChoices);
      message.appendChild(messageReactions);
      chatContainer.appendChild(message);
      chatContainer.scrollTop = chatContainer.scrollHeight + 100;
    } else if (data.type === 'message_reaction') {
      let reactions = data.reactions;
      let message_id = data.message_id;
      let container = $(`.message__reactions--container[data-message-id=${message_id}]`);
      container.html('');
      if (reactions) {
        for (let reaction in reactions) {
          let reaction_emoji = document.createElement('img');
          reaction_emoji.classList.add('reaction_emoji--img');
          reaction_emoji.src = reaction;
          reaction_emoji.setAttribute('data-message-id', message_id);
          let reaction_count = document.createElement('span');
          reaction_count.classList.add('reactions__count');
          reaction_count.innerHTML = reactions[reaction].length;
          let reaction_item = document.createElement('div');
          reaction_item.classList.add('reaction-item');
          // add title attribute to reaction_item
          reaction_item.setAttribute('title', `Users reacted like this: ${reactions[reaction].join(', ')}`);
          if (reactions[reaction].includes(username)) {
            reaction_item.classList.add('reacted');
          }
          reaction_item.appendChild(reaction_emoji);
          reaction_item.appendChild(reaction_count);
          container.append(reaction_item);
          // restore event listeners
          reaction_emoji.addEventListener('click', reactionHandler);
        }
      }
    }
  };

  
  sendButton.addEventListener('click', function (e) {
    let sendAnonymously = sendAnonymouslyCheckbox.checked;
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const fileReader = new FileReader(file);
      fileReader.readAsDataURL(file);
      fileReader.onload = function (e) {
        const fileUrl = e.target.result;
        const chatMessage = {
          'type': 'chat_message',
          'chat_id': chatId,
          'message': linkifyHtml(chatInput.value),
          'username': sendAnonymously ? 'Anonymous' : username,
          'image': fileUrl
        };
        chatSocket.send(JSON.stringify(chatMessage));
        fileInput.value = '';
        chatInput.value = '';
        $('.emojionearea-editor').html('');
      };
    } else if (chatInput.value || $('.emojionearea-editor').html()) {
      const chatMessage = {
        'type': 'chat_message',
        'chat_id': chatId,
        'message': linkifyHtml(chatInput.value) || $('.emojionearea-editor').html(),
        'username': sendAnonymously ? 'Anonymous' : username,
        'image': null
      };
      chatSocket.send(JSON.stringify(chatMessage));
      chatInput.value = '';
      $('.emojionearea-editor').html('');
    } else {
      console.log('No message to send');
      // show some tooltip or something
      $('.emojionearea-editor').effect('highlight', {color: '#7272ccba'}, 1000);
    }
  });


  const reactionHandler = (e) => {
    $('.reactions__choices').addClass('hidden');
    let messageId = $(e.target).data('message-id');
    let emojiUrl = $(e.target).attr('src');
    let data = {
      'type': 'message_reaction',
      'message_id': messageId,
      'username': username,
      'emoji_url': emojiUrl
    };
    chatSocket.send(JSON.stringify(data));
  };
  $('.reaction_emoji--img').click(reactionHandler);



  document.getElementsByTagName('footer')[0].style.display = 'none';


});