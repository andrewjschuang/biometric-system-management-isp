from flask import Flask, request, redirect, url_for
import io
import cv2
import numpy as np
import psutil
import threading

import Recognition
import fr_encodings
import config

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
recognition = Recognition.Recognition()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No image received\n'
        image = request.files['file']

        if image.filename == '':
            return 'No selected image\n'

        if image and allowed_file(image.filename):
            in_memory_file = io.BytesIO()
            image.save(in_memory_file)
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            img = cv2.imdecode(data, color_image_flag)

            found = recognition.recognize(img)
            return str(found)

    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Envie uma foto para reconhecimento facial</p>
            <form method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <input type=submit value=Enviar>
            </form>
            '''

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No image received\n'
        image = request.files['file']

        if image.filename == '':
            return 'No selected image\n'

        if image and allowed_file(image.filename):
            in_memory_file = io.BytesIO()
            image.save(in_memory_file)
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            img = cv2.imdecode(data, color_image_flag)
            name = request.form['name']

            if fr_encodings.persist(img, name):
                return 'Cadastro para %s salvo' % name
            else:
                return 'Erro no cadastro de %s' % name

    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Envie uma foto para cadastrar</p>
            <form method=post enctype=multipart/form-data>
            <p>Nome:</p>
            <p><input type="text" name="name"></p>
            <p><input type=file name=file></p>
            <input type=submit value=Enviar>
            </form>
            '''

@app.route('/capture', methods=['GET'])
def capture():
    video_source = request.args.get('source', default=config.video_source)
    display_image = request.args.get('display', default=config.display_image)
    output = request.args.get('output', default=config.output)
    encodings = request.args.get('encodings', default=config.encodings)
    tolerance = request.args.get('tolerance', default=config.tolerance)

    recognition.update(video_source, display_image, output, encodings, tolerance)
    threading.Thread(target=recognition.start).start()

    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Gravando...</p>
            '''

@app.route('/stop', methods=['GET'])
def stop():
    p_name = 'flask'
    for proc in psutil.process_iter():
        if proc.name() == p_name:
            proc.kill()
    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Gravação finalizada</p>
            '''

if __name__ == '__main__':
    app.run()

# curl -X GET http://localhost:5000
# curl -F "file=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
