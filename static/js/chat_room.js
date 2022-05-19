document.addEventListener('DOMContentLoaded', function () {
  const roomName = document.getElementById('chat-room').value;
  const chatContainer = document.getElementsByClassName('chat-container')[0];
  const chatInput = document.getElementById('chat-input');
  const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const socketUrl = `${socketProtocol}//${window.location.host}/ws/chat/${roomName}/`;
  const chatSocket = new WebSocket(socketUrl);
  console.log(socketUrl);
  console.log(chatSocket)


})