from flask import Flask, request, redirect, url_for, render_template
import io
import cv2
import psutil
import threading
import numpy as np

import Recognition
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
            return render_template('found.html', found=found)

    return render_template('upload.html')

@app.route('/register', methods=['GET', 'POST'])
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
        
        return render_template('registered.html')

    return render_template('register.html')

@app.route('/capture', methods=['GET'])
def capture():
    video_source = request.args.get('source', default=config.video_source)
    display_image = request.args.get('display', default=config.display_image)
    tolerance = request.args.get('tolerance', default=config.tolerance)

    result = recognition.update(video_source, display_image, tolerance)
    if result is not None:
        return result
    else:
        threading.Thread(target=recognition.start).start()

    return render_template('capture.html')

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
