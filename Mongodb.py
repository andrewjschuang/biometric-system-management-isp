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

    def get_collection(self, collection):
        return self.db[collection]

    def insert(self, collection, documents):
        # document keys validation
        ids = self.db[collection].insert(documents)
        return ids

    def delete(self, collection, document):
        if type(document) == str:
            return self.db[collection].delete_many(self.getObjectIdDocument(document))
        else:
            return self.db[collection].delete_many(document)

    def delete_all(self, collection, confirmation=False):
        if confirmation:
            return self.delete(collection, {})
        else:
            print('ERROR: confirmation is set to false')
            return None

    def find(self, collection, document):
        if type(document) == str:
            return self.db[collection].find(self.getObjectIdDocument(document))
        else:
            return self.db[collection].find(document)

    def increment(self, collection, document):
        if type(document) == str:
            return self.db[collection].update(self.getObjectIdDocument(document), { '$inc': { 'n': 1 } } )
        else:
            return self.db[collection].update_many( document, { '$inc' : { 'n': 1 } } )
