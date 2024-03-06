import config
from abc import ABC
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId

default_host = config.mongodb['host']
default_port = config.mongodb['port']
default_db_name = config.mongodb['db_name']


class MongoConnector(ABC):
    def __init__(self, host=default_host, port=default_port, db_name=default_db_name):
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.client[self.db_name]
        self.fs = GridFS(self.db)

    def __set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)

    def __object_id(self, document_id):
        return {'_id': ObjectId(document_id)}

    def __object_document(self, obj):
        try:
            return obj.to_dict()
        except:
            return obj

    def __get_all_documents(self):
        for document in self.collection.find():
            yield document

    def __insert(self, obj):
        # TODO: document keys validation
        document = self.__object_document(obj)
        return self.collection.insert_one(document)

    def __update(self, document_id, field, obj, operator, upsert=True):
        _id = self.__object_id(document_id)
        document = self.__object_document(obj)
        return self.collection.update_one(_id, {operator: {field: document}}, upsert)

    def __replace(self, document_id, obj):
        _id = self.__object_id(document_id)
        document = self.__object_document(obj)
        return self.collection.replace_one(_id, document)

    def __delete(self, obj):
        document = self.__object_document(obj)
        return self.collection.delete_one(document)

    def __delete_by_id(self, document_id):
        _id = self.__object_id(document_id)
        return self.collection.delete_one(_id)

    def __find(self, obj={}):
        document = self.__object_document(obj)
        if type(document) == str or type(document) == ObjectId:
            return self.collection.find(self.__object_id(document))
        return self.collection.find(document)

    def __find_by_id(self, document_id):
        _id = self.__object_id(document_id)
        return self.collection.find(_id)
