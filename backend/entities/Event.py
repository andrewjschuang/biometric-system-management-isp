class Event:
    def __init__(self, member_id, name, timestamp, face_distance, photo, encoding=None, confirmed=False):
        self.member_id = member_id
        self.name = name
        self.timestamp = timestamp
        self.face_distance = face_distance
        self.photo = photo
        self.encoding = encoding
        self.confirmed = confirmed

    def __str__(self):
        return 'Event(member_id=%s, name=%s, timestamp=%s, face_distance=%s, photo=%s, confirmed=%s)' % (self.member_id, self.name, self.timestamp, self.face_distance, self.photo, self.confirmed)

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'timestamp': self.timestamp,
            'face_distance': self.face_distance,
            'photo': self.photo,
            'confirmed': self.confirmed,
        }

    @staticmethod
    def from_dict(event):
        return Event(event['member_id'], event['name'], event['timestamp'], event['face_distance'], event['photo'], event.get('encoding'), event.get('confirmed'))
