from flask import Flask, request, redirect, url_for, render_template
import io
import cv2
import psutil
import datetime
import threading
import numpy as np

import Recognition
import config

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
recognition = Recognition.Recognition()

photo_labels = ['central', 'direita', 'esquerda']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_validation(request, filename='file'):
    if type(filename) == list:
        if len(request.files) == 0:
            return { 'error': True, 'message': 'no image received' }
        return { 'error': False }

    if filename not in request.files:
        return { 'error': True, 'message': 'no image received' }

    file = request.files['file']

    if file.filename == '':
            return { 'error': True, 'message': 'no selected image' }

    if not (file and allowed_file(file.filename)):
        return { 'error': True, 'message': 'file is not an image' }

    return { 'error': False }

def get_image(image):
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)

    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        result = image_validation(request)

        if result['error']:
            return render_template('error.html', error=result['message'])

        image = get_image(request.files['file'])
        found = recognition.recognize(image)

        return render_template('found.html', found=found)

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = image_validation(request, photo_labels)

        if result['error']:
            return render_template('error.html', error=result['message'])

        member = {key:request.form[key] for key in request.form if request.form[key]}
        member['data_foto'] = datetime.datetime.now().isoformat()
        member['fotos'] = {}

        images = request.files
        for image_label in images:
            image = get_image(images[image_label])
            face_locations, face_encodings = recognition.get_faces_from_picture(image)
            encoding = {
                'nome': member['nome'],
                'foto': face_encodings[0].tolist(),
                'obs': None
            }
            encoding_id = recognition.db.insert('encodings', encoding)
            member['fotos'][image_label] = encoding_id

        member_id = recognition.db.insert('members', member)
        recognition.get_known_encodings()

        return render_template('registered.html', name=member['nome'])

    return render_template('register.html', labels=photo_labels)

@app.route('/start', methods=['GET'])
def start():
    video_source = request.args.get('source', default=config.video_source)
    display_image = request.args.get('display', default=config.display_image)
    tolerance = request.args.get('tolerance', default=config.tolerance)

    result = recognition.update(video_source, display_image, tolerance)
    if result is not None:
        return result
    else:
        threading.Thread(target=recognition.start).start()

    return render_template('start.html')

@app.route('/stop', methods=['GET'])
def stop():
    p_name = 'flask'
    for proc in psutil.process_iter():
        if proc.name() == p_name:
            proc.kill()

    return render_template('stop.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# curl -X GET http://localhost:5000
# curl -F "file=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
