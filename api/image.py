import io
import cv2
import numpy as np
from recognition.Recognition import Recognition


recognition = Recognition()


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_validation(request):
    file = request.files.get('image')
    if not file:
        raise Exception('no image received')
    if not allowed_file(file.filename):
        raise Exception('file is not an image')


def get_image(image):
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    return cv2.imdecode(data, color_image_flag)


def recognize(request):
    image_validation(request)
    image = get_image(request.files.get('image'))
    results = recognition.recognize(image)
    return [result.to_dict() for result in results]
