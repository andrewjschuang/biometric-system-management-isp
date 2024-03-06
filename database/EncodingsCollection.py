from database.MongoConnector import MongoConnector
from entities.Encoding import Encoding


class EncodingsCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('encodings')

    def get_all_encodings(self):
        encodings = self._find()
        return [Encoding.from_dict(encoding) for encoding in encodings]

    def insert_encoding(self, encoding):
        return self._insert(encoding)

    def delete_encoding(self, _id):
        return self._delete_by_id(_id)
