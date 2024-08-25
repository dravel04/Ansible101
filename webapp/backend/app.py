from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])  # Permitir solicitudes desde http://127.0.0.1:3000

socketio = SocketIO(app, path='/api' ,cors_allowed_origins="http://127.0.0.1:3000")

@app.route('/')
def index():
    return ''

@socketio.on('message')
def handle_message(message):
    try:
        # Ejecutar el comando recibido
        result = subprocess.run(message, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        emit('response', output)
    except Exception as e:
        emit('response', str(e))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005)
