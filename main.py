from app_reso import create_app
from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

app = create_app()
Session(app)
socketio = SocketIO(app, manage_session=False)

@socketio.on('join', namespace='/chat')
def join(message):
    """
    Defines a SocketIO event call for when you join the chatroom

    :param message: the message upon user arrival to the room
    """
    defaultroom = session.get('room')
    join_room(defaultroom)
    emit('status', {'msg': session['username'] + ' has joined the chat'}, room=defaultroom)


@socketio.on('text', namespace='/chat')
def text(message):
    """
    Defines a SocketIO event call for when user sends a message

    :param message: username along with their entered message
    """
    defaultroom = session.get('room')
    emit('message', {'msg': session['username'] + ': ' + message['msg']}, room=defaultroom)
    # Broadcast message to all clients

@socketio.on('left', namespace='/chat')
def left(message):
    """
    Defines a SocketIO event call for when user leaves room

    :param message: user x has left the room
    """
    username = session.get('username')
    defaultroom = session.get('room')
    print(username, defaultroom)
    leave_room(defaultroom)
    # session.clear()
    emit('status', {'msg': username + ' has left the chat'}, room=defaultroom)
    # Broadcast to clients to inform them that x has left


if __name__ == '__main__':
    socketio.run(app, debug=True)