class Name():

    def __init__(self, last_name, first_name, middle_name=''):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name

    def __str__(self):
        if middle_name == '':
            return 'Name(first_name=%s, last_name=%s)' % (first_name, last_name)
        return 'Name(first_name=%s, middle_name=%s, last_name=%s)' % (first_name, middle_name, last_name)
