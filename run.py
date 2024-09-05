from app import create_app, socketio  # Import your app factory and socketio instance
from config import DevConfig  # Import your configuration

# Create the Flask app using the factory function
app = create_app(DevConfig)  # Pass the configuration class if needed

# Run the app with Socket.IO
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
