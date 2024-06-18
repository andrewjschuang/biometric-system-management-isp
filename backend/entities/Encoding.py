import numpy as np


class Encoding:
    def __init__(self, member_id, name, data):
        self.member_id = str(member_id)
        self.name = name
        self.data = data

    def __str__(self):
        return 'Encoding(member_id=%s, name=%s)' % (self.member_id, self.name)

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'data': self.data.tolist()
        }

    @staticmethod
    def from_dict(encoding):
        return Encoding(encoding['member_id'], encoding['name'], np.array(encoding['data']))
