import io
from base64 import b64encode
from PIL import Image
from api.image import get_image
from entities.Person import Person
from entities.Encoding import Encoding
from recognition.Recognition import Recognition


recognition = Recognition()


def _image_binary(image_bytes, resize=0.5):
    image = Image.open(io.BytesIO(image_bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0] * resize), int(image.size[1] * resize))
    image.thumbnail(new_size, Image.LANCZOS)
    image.save(imgByteArr, format='JPEG')
    imgByteArr.seek(0)
    return imgByteArr.getvalue()


def _get_person_image_from_bytes(bytes, resize):
    image = Image.open(io.BytesIO(bytes))
    imgByteArr = io.BytesIO()
    new_size = (int(image.size[0]*resize), int(image.size[0]*resize))
    image.thumbnail(new_size, Image.LANCZOS)
    image.save(imgByteArr, format='JPEG')
    return b64encode(imgByteArr.getvalue()).decode('utf-8')


def _create_person(data):
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


def _update_person_fields(form, person):
    person.name = form.get('name', person.name)
    person.birth_date = form.get('birth_date', person.birth_date)
    person.email = form.get('email', person.email)
    person.gender = form.get('gender', person.gender)
    person.phone_number = form.get('phone_number', person.phone_number)
    person.is_member = form.get('is_member', person.is_member)  # TODO: fix
    person.ministry = form.get('ministry', person.ministry)
    person.sigi = int(form.get('sigi') or person.sigi)
    return person


def _save_photos_from_request(images, person, member_id):
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


def get_members(request):
    members = recognition.members_db.get_all_members()
    return {'members': [x.to_dict() for x in members]}


def get_image_from_db(request, _id):
    image_bytes = recognition.images_db.get_image(_id)
    return _image_binary(image_bytes)


def create_member(request):
    person = _create_person(request.form)
    member_id = recognition.members_db.insert_member(person)
    try:
        _save_photos_from_request(request.files, person, member_id)
        recognition.members_db.replace_member(member_id, person)
        recognition.get_known_encodings()
    except Exception as e:
        recognition.members_db.delete_member(member_id)
        raise e


def update_member(request):
    member_id = request.form.get('id')
    person = recognition.members_db.get_member_by_id(member_id)
    person = _update_person_fields(request.form, person)
    _save_photos_from_request(request.files, person, person.id)
    recognition.members_db.replace_member(person.id, person)
    recognition.get_known_encodings()


def delete_member(request, _id):
    member = recognition.members_db.get_member_by_id(_id)
    recognition.members_db.delete_member(_id)
    for key in member.photos:
        recognition.images_db.delete_image(member.photos[key])
    for key in member.encodings:
        recognition.encodings_db.delete_encoding(member.encodings[key])
