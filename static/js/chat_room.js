/* jshint esversion: 6 */
document.addEventListener('DOMContentLoaded', function () {
  const roomName = window.location.pathname.split('/')[2];
  const chatContainer = document.getElementsByClassName('chat-container')[0];
  const chatInput = document.getElementById('chat-input');
  const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const socketUrl = `${socketProtocol}//${window.location.host}/ws/chat/${roomName}/`;
  const chatSocket = new WebSocket(socketUrl);
  
  const chatId = document.getElementById('chat-id').value;
  const username = document.getElementById('username').value;


  chatSocket.onopen = function () {
    console.log('Connected to chat server');
  };

  chatSocket.onclose = function () {
    console.log('Disconnected from chat server');
  };

  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log(data);
   
    let messageHtml = `<div class="message">
    <div class="message-header">
                <div class="message-header-username">
                    ${data.username}
                </div>
                <div class="message-header-time">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
            <div class="message-body">
                ${data.message}
            </div>
        </div>`;
    chatContainer.innerHTML += messageHtml;
  };

  document.addEventListener('keydown', function (e) {
    if(e.key == 'Enter') {
      console.log('Enter pressed');
      const chatMessage = {
        'chat_id': chatId,
        'message': chatInput.value,
        'username': "Anonymous"
      };
      chatSocket.send(JSON.stringify(chatMessage));
      chatInput.value = '';
    }
  });


})