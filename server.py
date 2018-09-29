from flask import Flask, request, redirect, url_for
import io
import cv2
import numpy as np
import psutil
import _thread

import video_capture
import config

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

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
            # filename = secure_filename(image.filename)
            in_memory_file = io.BytesIO()
            image.save(in_memory_file)
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            img = cv2.imdecode(data, color_image_flag)
            found = video_capture.identify_people(img)
            return str(found)
    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Selecionar foto</p>
            <form method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <input type=submit value=Enviar>
            </form>
            '''

@app.route('/capture', methods=['GET'])
def capture():
    _thread.start_new_thread(video_capture.main, (config.video_source, config.display_image, config.output, config.encodings, config.tolerance, True))
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
    return '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Gravação finalizada</p>
            '''

if __name__ == '__main__':
    app.run()

# curl -X GET http://localhost:5000
# curl -F "file=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
