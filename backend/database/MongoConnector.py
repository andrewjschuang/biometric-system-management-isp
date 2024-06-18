import config
from abc import ABC
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

default_host = config.mongodb['host']
default_port = config.mongodb['port']
default_db_name = config.mongodb['db_name']


class MongoConnector(ABC):
    def __init__(self, host=default_host, port=default_port, db_name=default_db_name):
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.client[self.db_name]
        self.fs = GridFS(self.db)

    def _set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)

    def _object_id(self, document_id):
        return {'_id': ObjectId(document_id)}

    def _object_document(self, obj):
        try:
            return obj.to_dict()
        except:
            return obj

    def _get_all_documents(self):
        for document in self.collection.find():
            yield document

    def _insert(self, obj):
        # TODO: document keys validation
        document = self._object_document(obj)
        result = self.collection.insert_one(document)
        if not result.acknowledged:
            raise Exception("Failed to insert")
        return str(result.inserted_id)

    def _upsert(self, obj):
        if '_id' in obj:
            self._update(obj)
        else:
            self._insert(obj)

    def _update(self, document_id, field, obj, operator, upsert=True):
        _id = self._object_id(document_id)
        document = self._object_document(obj)
        result = self.collection.update_one(_id, {operator: {field: document}}, upsert)
        # TODO: return something?

    def _replace(self, document_id, obj):
        _id = self._object_id(document_id)
        document = self._object_document(obj)
        return str(self.collection.replace_one(_id, document))

    def _delete(self, obj):
        document = self._object_document(obj)
        return str(self.collection.delete_one(document))

    def _delete_by_id(self, document_id):
        _id = self._object_id(document_id)
        # TODO: return something?
        return str(self.collection.delete_one(_id))

    def _find(self, obj={}, projection=None):
        document = self._object_document(obj)
        if type(document) == str or type(document) == ObjectId:
            return self.collection.find(self._object_id(document), projection)
        return self.collection.find(document, projection)

    def _find_by_id(self, document_id):
        _id = self._object_id(document_id)
        return self.collection.find_one(_id)
