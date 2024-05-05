from database.MongoConnector import MongoConnector
from bson import ObjectId


class ImagesCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('images')

    # gets the image in grid fs by id
    def get_image(self, _id):
        if (type(_id) == str):
            _id = ObjectId(_id)
        return self.fs.get(_id).read()

    def insert_image(self, image):
        return str(self.fs.put(image))
