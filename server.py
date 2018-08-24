from flask import Flask, request
from werkzeug.utils import secure_filename

import video_capture

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return 'Hello!\n'
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image received\n'
        image = request.files['image']
        if image.filename == '':
            return 'No selected image\n'
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            return video_capture.identify_people(image, filename)

# curl -X GET http://localhost:5000
# curl -F "image=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
