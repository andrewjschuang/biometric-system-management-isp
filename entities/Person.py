from itertools import zip_longest

from entities.Name import Name
from entities.Day import Day
from entities.Ministry import Ministry
from entities.Calendar import Calendar
from entities.Encoding import Encoding
from entities.PhotoCategory import PhotoCategory
from entities.Sunday import Sunday


class Person:
    def __init__(self, id, name, birth_date, email, gender, phone_number, member, ministry, sigi, calendar, photos, encodings):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.email = email
        self.gender = gender
        self.phone_number = phone_number
        self.member = member
        self.ministry = ministry
        self.sigi = sigi
        self.calendar = calendar
        self.photos = photos
        self.encodings = encodings
        self.is_active = self.calendar.is_active()

    def __str__(self):
        return 'Person(id=%s, name=%s, birth_date=%s, email=%s, gender=%s, phone_number=%s, member=%s, ministry=%s, sigi=%s, calendar=%s, photos=%s, encodings=%s)' % (
            self.id, self.name, self.birth_date, self.email, self.gender, self.phone_number, self.member, self.ministry, self.sigi, self.calendar, self.photos, self.encodings)

    def set_id(self, id):
        self.id = id
        return self

    def set_sundays(self, sundays):
        for index, t in enumerate(zip_longest(self.calendar.sundays, sundays)):
            sunday = t[1]
            if sunday is not None:
                self.calendar.sundays[index] = sunday
        self.is_active = self.calendar.is_active()

    def to_dict(self):
        photos = {}
        if self.photos is not None:
            for x in self.photos:
                if hasattr(self.photos[x], 'to_dict'):
                    photos[x] = self.photos[x].to_dict()
                else:
                    photos[x] = self.photos[x]

        encodings = {}
        if self.encodings is not None:
            for x in self.encodings:
                if hasattr(self.encodings[x], 'to_dict'):
                    encodings[x] = self.encodings[x].to_dict()
                else:
                    encodings[x] = self.encodings[x]

        return {
            'id': self.id,
            'name': self.name.to_dict(),
            'birth_date': self.birth_date.to_dict(),
            'email': self.email,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'member': self.member,
            'ministry': [x.name for x in self.ministry],
            'sigi': self.sigi,
            'calendar': self.calendar.to_dict(),
            'photos': {(x.name if type(x) == PhotoCategory else x): str(photos[x]) for x in photos},
            'encodings': {(x.name if type(x) == PhotoCategory else x): str(encodings[x]) for x in encodings}
        }

    @staticmethod
    def from_dict(person):
        ministry = [Ministry[x] for x in person['ministry']]
        return Person(str(person['_id']), Name.from_dict(person['name']), Day.from_dict(person['birth_date']), person['email'], person['gender'],
                      person['phone_number'], person['member'], ministry, person['sigi'],
                      Calendar.from_dict(person['calendar']), person['photos'], person['encodings'])
