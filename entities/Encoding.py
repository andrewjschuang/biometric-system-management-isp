import numpy as np
from entities.Name import Name

class Encoding:

    def __init__(self, member_id, name, data):
        self.member_id = member_id
        self.name = name
        self.data = data

    def __str__(self):
        return 'Encoding(member_id=%s, name=%s)' % (self.member_id, self.name)

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name.to_dict(),
            'data': self.data
        }

    @staticmethod
    def from_dict(encoding):
        return Encoding(encoding['member_id'], Name.from_dict(encoding['name']), np.array(encoding['data']))
