class Person:

    def __init__(self, name, birth_date, email, gender, phone_number, member, ministry, sigi, calendar, photos, encodings):
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

    def is_active(self):
        return self.calendar.is_active()

    def __str__(self):
        return 'Person(name=%s, birth_date=%s, email=%s, gender=%s, phone_number=%s, member=%s, ministry=%s, sigi=%s, calendar=%s, photos=%s, encodings=%s)' % (
            self.name, self.birth_date, self.email, self.gender, self.phone_number, self.member, self.ministry, self.sigi, self.calendar, self.photos, self.encodings)

    def to_dict(self):
        photos = {}
        for x in self.photos:
            if hasattr(self.photos[x], 'to_dict'):
                photos[x] = self.photos[x].to_dict()
            else:
                photos[x] = self.photos[x]

        encodings = {}
        for x in self.encodings:
            if hasattr(self.encodings[x], 'to_dict'):
                encodings[x] = self.encodings[x].to_dict()
            else:
                encodings[x] = self.encodings[x]

        return {
            'name': self.name.to_dict(),
            'birth_date': self.birth_date.to_dict(),
            'email': self.email,
            'gender': self.gender.name,
            'phone_number': self.phone_number,
            'member': self.member,
            'ministry': [x.name for x in self.ministry],
            'sigi': self.sigi,
            'calendar': self.calendar.to_dict(),
            'photos': { x.name : photos[x] for x in photos },
            'encodings': { x.name : encodings[x] for x in encodings }
        }
