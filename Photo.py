class Photo:

    def __init__(self, photo_category, photo_mode, size, data):
        self.photo_category = photo_category
        self.photo_mode = photo_mode
        self.size = size
        self.data = data

    def __str__(self):
        return 'Photo(photo_category=%s, photo_mode=%s, size=%s)' % (self.photo_category, self.photo_mode, self.size)
