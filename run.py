# run.py
import os
from flask_socketio import SocketIO

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
socketio = SocketIO(app)

if __name__ == '__main__':
    app.debug = True
    #app.run()
    socketio.run(app)
