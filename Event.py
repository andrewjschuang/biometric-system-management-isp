class Event:

    def __init__(self, member_id, name, day, face_distance, encoding, photo):
        self.member_id = member_id
        self.name = name
        self.day = day
        self.face_distance = face_distance
        self.encoding = encoding
        self.photo = photo

    def __str__(self):
        return 'Event(member_id=%s, name=%s, day=%s, face_distance=%s, encoding=%s)' % (self.member_id, self.name, self.day, self.face_distance, self.encoding)
