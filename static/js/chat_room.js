/* jshint esversion: 6 */
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
    let message = document.createElement('div');
    message.classList.add('message');
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
    messageHeaderUsername.innerHTML = data.username || 'Anonymous';
    messageHeaderTime.innerHTML = data.time;
    messageBodyText.innerHTML = data.message;
    if (data.image) {
      messageBodyImage.innerHTML = `<img src="${data.image}" />`;
    }
    // messageHeaderAvatar.innerHTML = `<img src="${data.avatar}" />`;
    messageHeader.appendChild(messageHeaderData);
    messageHeaderData.appendChild(messageHeaderAvatar);
    messageHeaderData.appendChild(messageHeaderUsername);
    messageHeaderData.appendChild(messageHeaderTime);
    message.appendChild(messageHeader);
    message.appendChild(messageBody);
    messageBody.appendChild(messageBodyText);
    messageBody.appendChild(messageBodyImage);
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight + 100;
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
          'chat_id': chatId,
          'message': chatInput.value,
          'username': sendAnonymously ? 'Anonymous' : username,
          'image': fileUrl
        };
        chatSocket.send(JSON.stringify(chatMessage));
        fileInput.value = '';
        chatInput.value = '';
      };
    } else {
      const chatMessage = {
        'chat_id': chatId,
        'message': chatInput.value,
        'username': sendAnonymously ? 'Anonymous' : username,
        'image': null
      };
      chatSocket.send(JSON.stringify(chatMessage));
      chatInput.value = '';
    }
  });

  document.getElementById('footer').style.display = 'none';

});