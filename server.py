from flask import Flask, request
from werkzeug.utils import secure_filename
import io
import cv2
import numpy as np

import video_capture

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
            return video_capture.identify_people(img)
    return  '''
            <!doctype html>
            <title>Biometric System Management ISP</title>
            <p>Upload new File</p>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''

# curl -X GET http://localhost:5000
# curl -F "image=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
