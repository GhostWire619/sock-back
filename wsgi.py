from app import create_app,socketio
from config import ProdConfig
# from flask_socketio import SocketIO

app = create_app(ProdConfig)

# Expose the WSGI application callable

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
