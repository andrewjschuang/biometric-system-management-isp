import json
from itertools import zip_longest
# from entities.Calendar import Calendar


class Person:
    def __init__(self, id, name, birth_date, email, gender, phone_number, is_member, ministry, sigi, photos={}, encodings={}, calendar=None):
        self.id = str(id)
        self.name = name
        self.birth_date = birth_date
        self.email = email
        self.gender = gender
        self.phone_number = int(phone_number)
        self.is_member = is_member.lower() == 'true' if type(is_member) == str else is_member
        self.ministry = ministry
        self.sigi = int(sigi)
        self.photos = photos
        self.encodings = encodings
        # self.calendar = Calendar()
        # self.is_active = self.calendar.is_active()

    def __str__(self):
        return 'Person(id=%s, name=%s, birth_date=%s, email=%s, gender=%s, phone_number=%s, is_member=%s, ministry=%s, sigi=%s, photos=%s, encodings=%s, calendar=%s, is_active=%s)' % (
            self.id, self.name, self.birth_date, self.email, self.gender, self.phone_number, self.is_member, self.ministry, self.sigi, self.photos, self.encodings, self.calendar, self.is_active)

    def __str__(self):
        return 'Person(id=%s, name=%s, birth_date=%s, email=%s, gender=%s, phone_number=%s, is_member=%s, ministry=%s, sigi=%s, photos=%s, encodings=%s)' % (
            self.id, self.name, self.birth_date, self.email, self.gender, self.phone_number, self.is_member, self.ministry, self.sigi, self.photos, self.encodings)

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
        return {
            'id': self.id,
            'name': self.name,
            'birth_date': self.birth_date,
            'email': self.email,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'is_member': self.is_member,
            'ministry': self.ministry,
            'sigi': self.sigi,
            'photos': json.loads(json.dumps(self.photos)),
            'encodings': json.loads(json.dumps(self.encodings)),
            # 'calendar': self.calendar.to_dict(),
            # 'is_active': self.is_active,
        }

    # @staticmethod
    # def from_dict(person):
    #     return Person(str(person['_id']), person['name'], person['birth_date'], person['email'], person['gender'],
    #                   person['phone_number'], person['is_member'], person['ministry'], person['sigi'],
    #                   person['photos'], person['encodings']), Calendar.from_dict(person['calendar'])

    @staticmethod
    def from_dict(person):
        return Person(person['_id'], person['name'], person['birth_date'], person['email'], person['gender'],
                      person['phone_number'], person['is_member'], person['ministry'], person['sigi'],
                      person['photos'], person['encodings'])
