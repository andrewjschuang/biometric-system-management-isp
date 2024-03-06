from database.MongoConnector import MongoConnector
from entities.Encoding import Encoding


class EncodingsCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        self.__set_collection('encodings')

    def get_all_encodings(self):
        encodings = self.__find()
        return [Encoding.from_dict(encoding) for encoding in encodings]

    def insert_encoding(self, encoding):
        return self.__insert(encoding)

    def delete_encoding(self, _id):
        return self.__delete_by_id(_id)
