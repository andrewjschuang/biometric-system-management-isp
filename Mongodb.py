from pymongo import MongoClient
from bson.objectid import ObjectId
from config import mongodb

class Mongodb:
    def __init__(self, host=mongodb['host'], port=mongodb['port'], db=mongodb['db']):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        self.db = self.client[db]

    def getObjectIdDocument(self, _id):
        return { '_id': ObjectId(_id) }

    def get_collection(self, collection, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        return coll

    def get_all(self, collection, db=None):
        cursor = self.get_collection(collection).find()
        return list(cursor)

    def get_member(self, id):
        return list(self.find('members', id))[0]

    def insert(self, collection, documents, db=None):
        # TODO: document keys validation
        coll = self.client[db][collection] if db else self.db[collection]
        ids = coll.insert(documents)
        return ids

    def delete(self, collection, document, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.delete_many(self.getObjectIdDocument(document))
        else:
            return coll.delete_many(document)

    def delete_all(self, collection, confirmation=False, db=None):
        if confirmation:
            return self.delete(collection, {}, db)
        else:
            print('ERROR: confirmation is set to false')
            return None

    def find(self, collection, document={}, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.find(self.getObjectIdDocument(document))
        else:
            return coll.find(document)

    def increment(self, collection, document, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.update(self.getObjectIdDocument(document), { '$inc': { 'n': 1 } } )
        else:
            return coll.update_many(document, { '$inc': { 'n': 1 } } )
