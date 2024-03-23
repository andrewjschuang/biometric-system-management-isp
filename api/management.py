import io
import re
from flask import render_template
from base64 import b64encode
from PIL import Image
from api.image import image_validation, get_image
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
from entities.Presence import Presence
from recognition.Recognition import Recognition


recognition = Recognition()
photo_labels = [
    PhotoCategory.FRONT.name,
    PhotoCategory.LEFT.name,
    PhotoCategory.RIGHT.name
]


def get_person_image_from_bytes(bytes, resize):
    image = Image.open(io.BytesIO(bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0]*resize), int(image.size[0]*resize))
    image.thumbnail(new_size, Image.LANCZOS)
    image.save(imgByteArr, format='JPEG')
    return b64encode(imgByteArr.getvalue()).decode('utf-8')


def create_person(form):
    name = Name.from_str(form.get('name'))
    birth_date = Day.from_str(form.get('birth_date'))
    email = form.get('email')
    gender = Gender[form.get('gender')]
    phone_number = phone_number = re.compile(
        '[\W_]+').sub('', form.get('phone_number'))
    member = form.get('member').lower() == 'true'
    ministry = [Ministry[form.get('ministry')]]
    sigi = int(form.get('sigi'))
    return Person(name, birth_date, email, gender, phone_number, member, ministry, sigi, Calendar(), {}, {})


def update_person_fields(form, person):
    person.name = Name.from_str(
        form.get('name')) if form.get('name') else person.name
    person.birth_date = Day.from_str(form.get('birth_date'))
    person.email = form.get('email') or person.email
    person.gender = Gender[form.get('gender')]
    person.phone_number = phone_number = re.compile(
        '[\W_]+').sub('', form.get('phone_number')) if form.get('phone_number') else person.phone_number
    person.member = form.get('member').lower() == 'true'
    person.ministry = [Ministry[form.get('ministry')]]
    person.sigi = int(form.get('sigi')) if form.get('sigi') else person.sigi
    return person


def index(request):
    persons = recognition.members_db.get_all_members()

    if request.method == 'POST':
        form = request.form.to_dict()
        date = Day.from_str(form.pop('presence_date'))
        presence = Presence[form.pop('presence')]
        ids = form.keys()  # gets ids to be marked

    for person in persons:
        try:
            image_bytes = recognition.images_db.get_image(
                person.encodings[PhotoCategory.FRONT.name])
            person.encodings[PhotoCategory.FRONT.name] = get_person_image_from_bytes(
                image_bytes, 0.05)
        except Exception as e:
            person.encodings[PhotoCategory.FRONT.name] = b''

        # if marking presence for person, update in database
        if request.method == 'POST':
            if str(person._id) in ids:
                if person.calendar.mark_presence(date, presence):
                    recognition.members_db.update_member_calendar(person)

    return render_template('management.html', persons=persons)


def get(request, _id):
    person = recognition.members_db.get_member_by_id(_id)
    images = []
    for encoding_id in person.encodings.values():
        try:
            image_bytes = recognition.images_db.get_image(encoding_id)
            image = get_person_image_from_bytes(image_bytes, 0.15)
            images.append(image)
        except Exception as e:
            print('failed to retrieve image: %s' % e)

    if request.method == 'POST':
        person = update_person_fields(request.form, person)
        person.set_sundays([Sunday.from_str(key.split('calendar.')[
                           1], request.form[key]) for key in request.form if 'calendar' in key])
        recognition.members_db.update_member_calendar(person)
        recognition.members_db.replace_member(person._id, person)

    return render_template('person.html', person=person, images=images, today=Day.today())


def delete(request, _id):
    try:
        member = recognition.members_db.get_member_by_id(_id)
        recognition.members_db.delete_member(_id)
        for key in member.encodings:
            recognition.encodings_db.delete_encoding(member.encodings[key])
    except Exception as e:
        print('error deleting member: %s' % e)
    return render_template('deleted.html')


def register(request):
    if request.method == 'POST':
        result = image_validation(request, photo_labels)

        if result['error']:
            return render_template('error.html', error=result['message'])

        person = create_person(request.form)
        member_id = recognition.members_db.insert_member(person)

        images = request.files
        for image_label in images:
            try:
                image = get_image(images[image_label])
                face_locations, face_encodings = recognition.get_faces_from_picture(
                    image)

                if len(face_encodings) == 0:
                    return render_template('error.html', error='no face found')
                if len(face_encodings) > 1:
                    return render_template('error.html', error='more than one face found')

                encoding = Encoding(member_id, person.name, face_encodings[0])
                encoding_id = recognition.encodings_db.insert_encoding(
                    encoding)

                imgByteArr = io.BytesIO()
                Image.open(images[image_label]).save(imgByteArr, format='JPEG')
                image_id = recognition.images_db.insert_image(
                    imgByteArr.getvalue())

                # may be broken
                person.encodings[PhotoCategory[image_label]] = encoding_id
                person.photos[PhotoCategory[image_label]] = image_id
            except Exception as e:
                print('failed to retrieve image: %s. reason: %s' %
                      (image_label, e))

        recognition.members_db.replace_member(member_id, person)
        recognition.get_known_encodings()

        return render_template('registered.html', name=person.name)

    return render_template('register.html', labels=photo_labels)
