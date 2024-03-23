from flask import Flask, request, redirect, url_for, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from recognition.Recognition import Recognition
import api.configuration as api_configuration
import api.image as api_image
import api.management as api_management
import api.signaling as api_signaling
import api.websocket as api_websocket
import base64
import time


app = Flask(__name__)
CORS(app)  # TOOD: remove?
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5173'])
recognition = Recognition()
recognition.inject_socket(socketio)


@socketio.on('connect')
def websocket_connect():
    return


@socketio.on('disconnect')
def websocket_disconnect():
    return


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('management'))


@app.route('/management', methods=['GET', 'POST'])
def management():
    return api_management.index(request)


@app.route('/management/<_id>', methods=['GET', 'POST'])
def get(_id):
    return api_management.get(request, _id)


@app.route('/management/delete/<_id>')
def delete(_id):
    return api_management.delete(request, _id)


@app.route('/management/register', methods=['GET', 'POST'])
def register():
    return api_management.register(request)


@app.route('/recognize', methods=['POST'])
def recognize():
    return api_image.recognize(request)


@app.route('/configure', methods=['GET', 'POST'])
def configure():
    try:
        config = api_configuration.configure(request)
        return jsonify({'data': config}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/start', methods=['GET'])
def start():
    api_signaling.start()
    return jsonify({'data': {'success': True}}), 200


@app.route('/stop', methods=['GET'])
def stop():
    api_signaling.stop()
    return jsonify({'data': {'success': True}}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=True)
