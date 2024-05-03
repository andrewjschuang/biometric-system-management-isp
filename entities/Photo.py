class Photo:
    def __init__(self, photo_category, photo_mode, data, size):
        self.photo_category = photo_category
        self.photo_mode = photo_mode
        self.data = data
        self.size = size

    def __str__(self):
        return 'Photo(photo_category=%s, photo_mode=%s, size=%s)' % (self.photo_category, self.photo_mode, self.size)

    def to_dict(self):
        return {
            'photo_category': self.photo_category.name,
            'photo_mode': self.photo_mode.name,
            'data': self.data,
            'size': self.size,
        }
