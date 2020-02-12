class Name:

    def __init__(self, last_name, first_name, middle_name=''):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name

    def __str__(self):
        if self.middle_name is None or self.middle_name == '':
            return '%s %s' % (self.first_name, self.last_name)
        return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)

    def __repr__(self):
        if self.middle_name == '':
            return 'Name(first_name=%s, last_name=%s)' % (self.first_name, self.last_name)
        return 'Name(first_name=%s, middle_name=%s, last_name=%s)' % (self.first_name, self.middle_name, self.last_name)

    def to_dict(self):
        if self.middle_name == '':
            return {
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        else:
            return {
                'first_name': self.first_name,
                'middle_name': self.middle_name,
                'last_name': self.last_name
            }

    @staticmethod
    def from_dict(name):
        return Name(name['last_name'], name['first_name'], name.get('middle_name'))
