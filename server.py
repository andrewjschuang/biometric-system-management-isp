from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from recognition.Recognition import Recognition
import api.configuration as api_configuration
import api.image as api_image
import api.management as api_management
import api.signaling as api_signaling
import api.event as api_event


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
CORS(app, origins=["http://localhost:5173"])  # TOOD: remove?
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5173'])
recognition = Recognition()
recognition.inject_socket(socketio)


@socketio.on('connect')
def websocket_connect():
    return


@socketio.on('disconnect')
def websocket_disconnect():
    return


@app.route('/start', methods=['GET'])
def start():
    api_signaling.start()
    return jsonify({'data': {'success': True}}), 200


@app.route('/stop', methods=['GET'])
def stop():
    api_signaling.stop()
    return jsonify({'data': {'success': True}}), 200


@app.route('/api/members', methods=['GET', 'POST', 'PUT'])
def members():
    if request.method == 'GET':
        data = api_management.get_members(request)
        return jsonify({'data': data}), 200
    elif request.method == 'POST':
        api_management.create_member(request)
        return jsonify({'data': 'success'}), 200
    elif request.method == 'PUT':
        api_management.update_member(request)
        return jsonify({'data': 'success'}), 200


@app.route('/api/members/<_id>', methods=['GET', 'DELETE'])
def members_by_id(_id):
    if request.method == 'GET':
        data = api_management.get_member(request, _id)
        return jsonify({'data': data}), 200
    if request.method == 'DELETE':
        api_management.delete_member(request, _id)
        return jsonify({'data': 'success'}), 200


@app.route('/api/images/<_id>', methods=['GET'])
def api_management_image(_id):
    image = api_management.get_image_from_db(request, _id)
    return Response(response=image, status=200, mimetype='image/jpeg')


@app.route('/api/events', methods=['GET'])
def get_events():
    data = api_event.get_events(request)
    return jsonify({'data': data}), 200


@app.route('/api/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'GET':
        config = api_configuration.get_configuration(request)
        return jsonify({'data': config}), 200
    elif request.method == 'POST':
        try:
            config = api_configuration.update_configuration(request)
            return jsonify({'data': config}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@app.route('/api/recognize', methods=['POST'])
def recognize():
    try:
        result = api_image.recognize(request)
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    try:
        if request.method == 'GET':
            result = api_configuration.get_settings(request)
        elif request.method == 'POST':
            result = api_configuration.update_settings(request)
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=True)
