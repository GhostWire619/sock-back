from flask import Blueprint, jsonify,request
from flask_cors  import cross_origin
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_bp.route('/register', methods=['POST'])
@cross_origin() 
def register():
    from app.models import User
    
    userName = request.json.get('userName')
    password = request.json.get('password')
    
    if User.query.filter_by(userName=userName).first():
        return jsonify({"msg": "userName already exists"}), 400
   # Hash the password
    if not password:
        return jsonify({'message': 'Password is required.'}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(
        userName=userName,
        password=hashed_password,
        )

    # Save the user to the database

    new_user.save()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
@cross_origin() 
def login():
    from app.models import User
    userName = request.json.get('userName')
    password = request.json.get('password')

    user = User.query.filter_by(userName=userName).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify(id= user.id,profData={"userName": user.userName}), 200
        
    else:
        return jsonify({"msg": "Invalid credentials"}), 401



@auth_bp.route('/register/room', methods=['POST'])
@cross_origin() 
def registerRoom():
    from app.models import Room
    
    title = request.json.get('title')
    user_id =request.json.get('user_id')
    
    if Room.query.filter_by(title=title).first():
        return jsonify({"msg": "Room already exists"}), 400

    # Create a new user
    new_room = Room(
        title=title,
        user_id=user_id
        )

    # Save the user to the database
    new_room.save()

    return jsonify({"msg": "Room registered successfully"}), 201


@auth_bp.route('/login/room', methods=['POST'])
@cross_origin() 
def loginRoom():
    from app.models import Room
    title = request.json.get('title')

    room = Room.query.filter_by(title=title).first()
    if room:
        # Convert room messages to a serializable format
        messages_list = [message_to_dict(message) for message in room.messages]
        
        return jsonify(id=room.id, title=room.title, messages=messages_list), 200
    

def message_to_dict(message):
    """Helper function to convert Message object to dictionary."""
    return {
        'id': message.id,
         'text': message.text,
        # 'createdAt': message.createdAt.isoformat(),  # Convert datetime to ISO format string
        'userName': message.sender.userName,
        # 'room_id': message.room_id
    }


@auth_bp.route('/rooms/<int:user_id>', methods=['GET'])
def get_user_rooms(user_id):
    from app.models import User,Room
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    rooms = Room.query.filter_by(user_id=user_id).all()
    rooms_list = [{"id": room.id, "title": room.title} for room in rooms]

    return jsonify(rooms_list), 200