from flask import Flask, request, redirect, url_for, render_template
from base64 import b64encode
import io
import re
import cv2
import json
import time
import datetime
import threading
import numpy as np
from PIL import Image

import config
from recognition.Recognition import Recognition
from entities.Person import Person
from entities.PhotoCategory import PhotoCategory
from entities.Calendar import Calendar
from entities.Day import Day
from entities.Sunday import Sunday
from entities.Gender import Gender
from entities.Ministry import Ministry
from entities.Encoding import Encoding
from entities.Collections import Collections
from entities.Name import Name
from entities.Event import Event

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
recognition = Recognition()

photo_labels = [
    PhotoCategory.FRONT.name,
    PhotoCategory.LEFT.name,
    PhotoCategory.RIGHT.name
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def get_person_image_from_bytes(bytes, resize):
    image = Image.open(io.BytesIO(bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0]*resize), int(image.size[0]*resize))
    image.thumbnail(new_size, Image.ANTIALIAS)
    image.save(imgByteArr, format='JPEG')
    return b64encode(imgByteArr.getvalue()).decode('utf-8')

def create_person(form):
    name = Name.from_str(form.get('name'))
    birth_date = Day.from_str(form.get('birth_date'))
    email = form.get('email')
    gender = Gender[form.get('gender')]
    phone_number = phone_number = re.compile('[\W_]+').sub('', form.get('phone_number'))
    member = form.get('member').lower() == 'true'
    ministry = [Ministry[form.get('ministry')]]
    sigi = int(form.get('sigi'))
    return Person(name, birth_date, email, gender, phone_number, member, ministry, sigi, Calendar(), {}, {})

def update_person_fields(form, person):
    person.name = Name.from_str(form.get('name')) if form.get('name') else person.name
    person.birth_date = Day.from_str(form.get('birth_date'))
    person.email = form.get('email') or person.email
    person.gender = Gender[form.get('gender')]
    person.phone_number = phone_number = re.compile('[\W_]+').sub('', form.get('phone_number')) if form.get('phone_number') else person.phone_number
    person.member = form.get('member').lower() == 'true'
    person.ministry = [Ministry[form.get('ministry')]]
    person.sigi = int(form.get('sigi')) if form.get('sigi') else person.sigi
    return person

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        result = image_validation(request)

        if result['error']:
            return render_template('error.html', error=result['message'])

        image = get_image(request.files['file'])
        events = recognition.recognize(image, day=request.form.get('day'), presence=request.form.get('presence'))
        found = [event.name for event in events]

        return render_template('found.html', found=found)

    return render_template('recognize.html')

@app.route('/api', methods=['POST'])
def api():
    result = image_validation(request)

    if result['error']:
        return json.dumps({ 'error': result['message'] })

    image = get_image(request.files['file'])
    events = recognition.recognize(image, update_presence=request.form.get('update'))

    return json.dumps({ 'results': events })

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = image_validation(request, photo_labels)

        if result['error']:
            return render_template('error.html', error=result['message'])

        person = create_person(request.form)
        member_id = recognition.db.insert_member(person)

        images = request.files
        for image_label in images:
            try:
                image = get_image(images[image_label])
                face_locations, face_encodings = recognition.get_faces_from_picture(image)

                if len(face_encodings) == 0:
                    return render_template('error.html', error='no face found')
                if len(face_encodings) > 1:
                    return render_template('error.html', error='more than one face found')

                encoding = Encoding(member_id, person.name, face_encodings[0])
                encoding_id = recognition.db.insert_encoding(encoding)

                imgByteArr = io.BytesIO()
                Image.open(images[image_label]).save(imgByteArr, format='JPEG')
                image_id = recognition.db.insert_image(imgByteArr.getvalue())

                # may be switched
                person.encodings[PhotoCategory[image_label]] = image_id
                person.photos[PhotoCategory[image_label]] = encoding_id
            except Exception as e:
                print('failed to retrieve image: %s. reason: %s' % (image_label, e))

        recognition.db.replace_member(member_id, person)
        recognition.get_known_encodings()

        return render_template('registered.html', name=person.name)

    return render_template('register.html', labels=photo_labels)

@app.route('/start', methods=['GET'])
def start():
    if not recognition.run:
        recognition.signal_handler(run=True)
        threading.Thread(target=recognition.start).start()
    return render_template('start.html')

@app.route('/stop', methods=['GET'])
def stop():
    recognition.signal_handler()
    return render_template('stop.html')

@app.route('/management', methods=['GET'])
def management():
    persons = recognition.db.get_all_members()
    for person in persons:
        try:
            image_bytes = recognition.db.get_image(person.encodings[PhotoCategory.FRONT.name])
            person.encodings[PhotoCategory.FRONT.name] = get_person_image_from_bytes(image_bytes, 0.05)
        except Exception as e:
            person.encodings[PhotoCategory.FRONT.name] = b''
    return render_template('management.html', persons=persons)

@app.route('/management/<_id>', methods=['GET', 'POST'])
def get(_id):
    person = recognition.db.get_member_by_id(_id)
    images = []
    for encoding_id in person.encodings.values():
        try:
            image_bytes = recognition.db.get_image(encoding_id)
            image = get_person_image_from_bytes(image_bytes, 0.15)
            images.append(image)
        except Exception as e:
            print('failed to retrieve image: %s' % e)

    if request.method == 'POST':
        person = update_person_fields(request.form, person)
        person.set_sundays([Sunday.from_str(key.split('calendar.')[1], request.form[key]) for key in request.form if 'calendar' in key])
        recognition.db.update_member_calendar(person)
        recognition.db.replace_member(person._id, person)

    return render_template('person.html', person=person, images=images, today=Day.today())

@app.route('/management/delete/<_id>')
def delete(_id):
    try:
        member = recognition.db.get_member_by_id(_id)
        recognition.db.delete_member(_id)
        for key in member.encodings:
            recognition.db.delete_encoding(member.encodings[key])
    except Exception as e:
        print('error deleting member: %s' % e)
    return render_template('deleted.html')

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        video_source = request.form.get('video_source')
        tolerance = request.form.get('tolerance')
        active_rate = request.form.get('active_rate')

        error = recognition.configure(video_source=video_source, tolerance=tolerance)
        if error is None:
            config.video_source = video_source
            config.tolerance = tolerance
            config.active_rate = active_rate
        return render_template('updated.html', error=error)

    return render_template('configure.html', config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# curl -X GET http://localhost:5000
# curl -F "file=@/home/andrewjschuang/dev/biometric-system-management/photos_for_encoding/random/andrew.jpg" -X POST http://localhost:5000
