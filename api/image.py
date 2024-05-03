import io
import cv2
import json
import numpy as np


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def image_validation(request, filename='file'):
    if type(filename) == list:
        if len(request.files) == 0:
            return {'error': True, 'message': 'no image received'}
        return {'error': False}

    if filename not in request.files:
        return {'error': True, 'message': 'no image received'}

    file = request.files['file']

    if file.filename == '':
        return {'error': True, 'message': 'no selected image'}

    if not (file and allowed_file(file.filename)):
        return {'error': True, 'message': 'file is not an image'}

    return {'error': False}


def get_image(image):
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    return img


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def recognize(request):
#     result = image_validation(request)

#     if result['error']:
#         return json.dumps({'error': result['message']})

#     image = get_image(request.files['file'])
#     events = recognition.recognize(
#         image, update_presence=request.form.get('update'))

#     return json.dumps({'results': events})
