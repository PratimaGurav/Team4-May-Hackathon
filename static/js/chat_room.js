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
    'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-thumbs-up_rtp2ny.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-scream_xkjxg7.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/party-cry_sgfigm.gif',
    'https://res.cloudinary.com/lexach91/image/upload/v1653110066/emojis/giphy-joy_oxskf3.gif'
  ];

  const hideReactions = () => {
    $('.reactions__choices').addClass('hidden');
  };

  $('.reactions__toggle').click(function (e) {
    e.stopPropagation();
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
      messageHeaderUsername.innerHTML = `<a class="message__header--username message__header--link" href="/profile/${data.username}/">${data.username}</a>` || 'Anonymous';
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
      console.log(data);
      let reactions = data.reactions;
      console.log(reactions);
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

  // document.addEventListener('keydown', function (e) {
  //   if(e.key == 'Enter') {
  //     console.log('Enter pressed');
  //     const chatMessage = {
  //       'chat_id': chatId,
  //       'message': chatInput.value,
  //       'username': username
  //     };
  //     chatSocket.send(JSON.stringify(chatMessage));
  //     chatInput.value = '';
  //   }
  // });

  sendButton.addEventListener('click', function (e) {
    // need to check if send anonymously is checked
    let sendAnonymously = sendAnonymouslyCheckbox.checked;
    // need to check if file is selected
    console.log('Send button clicked');
    if (fileInput.files.length > 0) {
      console.log('File selected');
      // we need to temporarily store the file in the local storage
      // so that we can send its url to the consumer over the socket
      // and then we can remove it from the local storage
      const file = fileInput.files[0];
      const fileReader = new FileReader(file);
      fileReader.readAsDataURL(file);
      fileReader.onload = function (e) {
        console.log(e.target.result);
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
      };
    } else if (chatInput.value) {
      const chatMessage = {
        'type': 'chat_message',
        'chat_id': chatId,
        'message': linkifyHtml(chatInput.value),
        'username': sendAnonymously ? 'Anonymous' : username,
        'image': null
      };
      chatSocket.send(JSON.stringify(chatMessage));
      chatInput.value = '';
    } else {
      console.log('No message to send');
      // show some tooltip or something
      $(chatInput).effect('highlight', {
        color: '#7272ccba'
      }, 1000);
    }
  });


  const reactionHandler = (e) => {
    console.log('Reaction clicked');
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