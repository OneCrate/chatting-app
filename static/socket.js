var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat'); // Initializes connection with our backend
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {         // Defines an Socketio event to display users status
    console.log(data)
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {       // Defines an Socketio event to display incoming messages
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#send').click(function(e) {      // Button event call for acquire user input message
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});   // Calls the socketio 'text' event in our backend
    });
});
function leave_room() {     // Defines a function to hanlde the leaving process
    socket.emit('left', {}, function() {    // Calls the socketio 'left' event in our backend
        console.log('leaving')
        socket.disconnect();
        window.location.href = "/room", true;
    });
}