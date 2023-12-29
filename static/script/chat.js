var socket = io.connect()

function joinRoom() {
    var room = document.getElementById('roomID').value;
    socket.emit('join', {'room': room});
}

function leaveRoom() {
    var room = document.getElementById('roomID').value;
    socket.emit('leave', {'room': room});
    var messages = document.getElementById('chat-area');

    var divs = messages.getElementsByTagName("div");

        for (var i = divs.length - 1; i >= 0; i--) {
            divs[i].remove();
        }
    location.reload()
}

function sendMessage() {
    var room = document.getElementById('roomID').value;
    var message = document.getElementById('text-message').value;
    socket.emit('message', {'room': room, 'msg': message});
    document.getElementById('text-message').value = '';
}

socket.on('mm', function(data) {
    var messages = document.getElementById('chat-area');

    var new_text_div = document.createElement("div");

    new_text_div.textContent = data['msg'];

    messages.append(new_text_div)
});