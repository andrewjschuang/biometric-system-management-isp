from database.MongoConnector import MongoConnector


class ImagesCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        self.__set_collection('images')

    # gets the image in grid fs by id
    def get_image(self, _id):
        return self.fs.get(_id).read()

    def insert_image(self, image):
        return self.fs.put(image)
