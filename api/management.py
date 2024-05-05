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


def image_binary(image_bytes, resize=0.5):
    image = Image.open(io.BytesIO(image_bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0] * resize), int(image.size[1] * resize))
    image.thumbnail(new_size, Image.LANCZOS)
    image.save(imgByteArr, format='JPEG')
    imgByteArr.seek(0)
    return imgByteArr.getvalue()


def get_person_image_from_bytes(bytes, resize):
    image = Image.open(io.BytesIO(bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0]*resize), int(image.size[0]*resize))
    image.thumbnail(new_size, Image.LANCZOS)
    image.save(imgByteArr, format='JPEG')
    return b64encode(imgByteArr.getvalue()).decode('utf-8')


def create_person(data):
    id = data.get('id')
    name = data.get('name')
    birth_date = data.get('birth_date')
    email = data.get('email')
    gender = data.get('gender')
    phone_number = data.get('phone_number')
    is_member = data.get('is_member')
    ministry = data.get('ministry')
    sigi = data.get('sigi')
    return Person(id, name, birth_date, email, gender, phone_number, is_member, ministry, sigi)


def save_photos_from_request(images, person, member_id):
    for image_label in images:
        image = get_image(images[image_label])
        _, face_encodings = recognition.get_faces_from_picture(image)
        if len(face_encodings) == 0:
            raise Exception(f'{image_label}: no face')
        if len(face_encodings) > 1:
            raise Exception(f'{image_label} more than one face')

        encoding = Encoding(member_id, person.name, face_encodings[0])
        encoding_id = recognition.encodings_db.insert_encoding(encoding)

        imgByteArr = io.BytesIO()
        Image.open(images[image_label]).save(imgByteArr, format='JPEG')
        image_id = recognition.images_db.insert_image(
            imgByteArr.getvalue())

        person.encodings[image_label] = encoding_id
        person.photos[image_label] = image_id


def update_person_fields(form, person):
    person.name = form.get('name', person.name)
    person.birth_date = form.get('birth_date', person.birth_date)
    person.email = form.get('email', person.email)
    person.gender = form.get('gender', person.gender)
    person.phone_number = form.get('phone_number', person.phone_number)
    person.member = form.get('member', str(person.member)).lower() == 'true'
    person.ministry = form.get('ministry', person.ministry)
    person.sigi = int(form.get('sigi', person.sigi))
    return person


def get_members(request):
    members = recognition.members_db.get_all_members()
    return {'members': [x.to_dict() for x in members]}


def update_member(request):
    person = create_person(request.form)
    save_photos_from_request(request.files, person, person.id)
    recognition.members_db.replace_member(person.id, person)
    recognition.get_known_encodings()


def register_api(request):
    person = create_person(request.form)
    member_id = recognition.members_db.insert_member(person)
    try:
        save_photos_from_request(request.files, person, member_id)
        recognition.members_db.replace_member(member_id, person)
        recognition.get_known_encodings()
    except Exception as e:
        recognition.members_db.delete_member(member_id)
        raise e


def get_image_from_db(request, _id):
    image_bytes = recognition.images_db.get_image(_id)
    return image_binary(image_bytes)


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
                person.photos['FRONT'])
            person.photos['FRONT'] = get_person_image_from_bytes(
                image_bytes, 0.05)
        except Exception as e:
            person.photos['FRONT'] = b''

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
