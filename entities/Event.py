class Event:
    def __init__(self, member_id, name, timestamp, face_distance, encoding, photo):
        self.member_id = member_id
        self.name = name
        self.timestamp = timestamp
        self.face_distance = face_distance
        self.encoding = encoding
        self.photo = photo

    def __str__(self):
        return 'Event(member_id=%s, name=%s, timestamp=%s, face_distance=%s, encoding=%s)' % (self.member_id, self.name, self.day, self.face_distance, self.encoding)

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'timestamp': self.timestamp,
            'face_distance': self.face_distance,
            'encoding': self.encoding.to_dict(),
            'photo': self.photo,
        }
