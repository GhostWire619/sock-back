from app import socketio
from flask import request
from flask_socketio import emit, join_room, leave_room
from .models import Room, User, Messages

# Track online users with socket IDs
online_users = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)
    # Attempt to re-associate the user with their previous session
    userName = get_user_by_sid(request.sid)
    if userName:
        online_users[userName] = request.sid
        emit('user_status', {'userName': userName, 'status': 'online'}, broadcast=True)
        print(f"User {userName} reconnected with SID {request.sid}")
    else:
        print('New client connected without an associated user')


@socketio.on('disconnect')
def handle_disconnect():
    userName = get_user_by_sid(request.sid)
    if userName:
        # Remove user from the online users dictionary
        del online_users[userName]
        # Notify all clients about user disconnection
        emit('user_status', {'userName': userName, 'status': 'offline'}, broadcast=True)
        print(f'User {userName} disconnected')
    else:
        print('Client disconnected without an associated user')

# Handle user connection
@socketio.on('user_connected')
def handle_user_connected(data):
    print(f"Received user_connected event with data: {data}")
    userName = data.get('userName')
    if userName:
        online_users[userName] = request.sid  # Map userName to socket ID
        print(f"User {userName} connected with SID {request.sid}")
        # Notify all clients about new user connection
        emit('user_status', {'userName': userName, 'status': 'online'}, broadcast=True)
    else:
        print("No userName provided in 'user_connected' event data.")

# Get userName from socket ID
def get_user_by_sid(sid):
    for userName, sid_map in online_users.items():
        if sid_map == sid:
            return userName
    return None

# Handle incoming messages
@socketio.on('send_message')
def handle_message(data):
    room_id = data.get('room_id')  # Assuming room_id is part of the message data
    room = data.get('room')
    text = data.get('message')
    userName = data.get('userName')

    if not room or not text or not userName:
        print("Incomplete data received for 'send_message' event.")
        return

    print(f"Message from {userName} in room {room}: {text}")
    # Emit the message to the room
    emit('receive_message', {'userName': userName, 'text': text}, room=room)

    # Find the user and room
    user = User.query.filter_by(userName=userName).first()
    room_ = Room.query.filter_by(title=room).first()

    if not user:
        print(f"User {userName} not found.")
        return
    
    if not room_:
        print(f"Room {room} not found.")
        return

    # Create a new message instance
    new_message = Messages(
        text=text,
        user_id=user.id,
        room_id=room_.id
    )

    # Save the message to the database
    new_message.save()

# Joining a chat room
@socketio.on('join')
def on_join(data):
    userName = data.get('userName')
    room = data.get('room')

    if not userName or not room:
        print("Incomplete data for 'join' event.")
        return

    join_room(room)
    print(f"User {userName} joined room {room}")
    emit('user_status', {'userName': userName, 'status': 'joined', 'room': room}, room=room)

# Leaving a chat room
@socketio.on('leave')
def on_leave(data):
    userName = data.get('userName')
    room = data.get('room')

    if not userName or not room:
        print("Incomplete data for 'leave' event.")
        return

    leave_room(room)
    print(f"User {userName} left room {room}")
    emit('user_status', {'userName': userName, 'status': 'left', 'room': room}, room=room)

@socketio.on('test_message')
def handle_test_message(data):
    print('Received test message:', data)
    emit('test_response', {'message': 'Hello from server!'})
