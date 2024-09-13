from flask import Flask,send_from_directory
from flask_socketio import SocketIO
from .exts import db
from flask_migrate import Migrate
from .auth import auth_bp
from flask_cors  import CORS

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins=["http://localhost:5173", "https://room-connect-8cf76c932125.herokuapp.com","https://room-chat-nzzm.onrender.com","https://room-chat.pages.dev"],
                    logger=True, engineio_logger=True)

def create_app(config=None):
    app = Flask(__name__, static_folder='static', static_url_path='')

    if config is None:
        config = 'config.DevConfig'

    app.config.from_object(config)

    # CORS configuration
    CORS(app, resources={
        r"/auth/*": {
            "origins": ["http://localhost:5173", "https://room-connect-8cf76c932125.herokuapp.com","https://room-chat-nzzm.onrender.com","https://room-chat.pages.dev"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"]
        },
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"]
        }
    })

    # Initialize other extensions
    db.init_app(app)
    Migrate(app, db)
    socketio.init_app(app)

    from app import sockets
    from .models import Room, User, Messages
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def serve_react_app():
        return send_from_directory(app.static_folder, 'index.html')

    # Example API route
    @app.route('/api/data')
    def get_data():
        return {"data": "Hello from Flask!"}

    return app

# Running the Flask application with SocketIO
if __name__ == "__main__":
    app = create_app()
    socketio.run(app)
